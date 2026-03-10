## King Halo - Writeup (WannaGame Championship)

### Mô tả

- Một thử thách về Zero-Knowledge Proof (ZKP) kết hợp với logic game đua ngựa (Uma Musume).
- Người chơi cần tương tác với server để chọn ngựa và đua. Để lấy được flag, cần phải chiến thắng liên tiếp 50 vòng.
- Ở mỗi vòng, server sẽ cung cấp danh sách ngựa đua, độ dài đường đua, `Merkle root` và một Merkle proof hợp lệ (dùng Halo2) cho con ngựa người chơi đã chọn.
- Sau khi có kết quả cuộc đua, người chơi cần cung cấp proof chứng minh con ngựa chiến thắng nằm trong Merkle tree và là của mình.

### Tệp đính kèm

- `src/` (mã nguồn Rust), `solve.py`, `Dockerfile`, `docker-compose.yml`, `Cargo.toml`, `Cargo.lock`.

### Phân tích

- **Lỗi logic khi kiểm tra lá (Leaf Verification Bypass):**
  Trong `server.rs`, đoạn code xác thực leaf của user được viết như sau:
  ```rust
  let provided_proof_result: io::Result<Vec<(bool, Fp)>> = provided_indices
      .into_iter()
      .zip(provided_elements.into_iter())
      .map(|(is_left, sibling)| {
          if leaves[provided_payload.index] != provided_leaf {
              return Err(...);
          }
          Ok((is_left, sibling))
      })
      .collect();
  ```
  Việc kiểm tra `leaves[index] == provided_leaf` nằm bên trong logic lặp `map()` của mảng proof. Nếu người chơi gửi lên một proof **rỗng** (mảng `[]`), closure này sẽ không bao giờ được gọi. Điều này cho phép người chơi chèn một `leaf` bất kỳ kèm `index` bất kỳ mà không bị server bắt lỗi.

- **Lỗi bypass độ sâu của proof:**
  Server gọi hàm `verify_proof(root, provided_leaf, &provided_proof, provided_proof.len())`. Do truyền trực tiếp `.len()` của mảng proof từ user vào thay vì `TREE_DEPTH`, hàm kiểm tra độ sâu trong `merkle.rs` mất đi tác dụng và chấp nhận proof có độ dài bằng 0.

- **Lỗ hổng trong mạch ZKP (Circuit accepts empty proof):**
  Trong `merkle_circuit.rs`:
  ```rust
  let mut digest: AssignedCell<Fp, Fp> = leaf_cell;
  for i in 0..self.path_elements.len() {
      digest = self.merkle_prove_layer(...) 
  }
  layouter.constrain_instance(digest.cell(), config.root_hash, 0)?;
  ```
  Khi người chơi đưa `path_elements` rỗng, vòng lặp hash bị bỏ qua hoàn toàn. Kết quả là hàm `constrain_instance` sẽ so sánh trực tiếp giá trị `leaf_cell` với `root_hash`. Do đó, nếu người chơi truyền `leaf` bằng đúng giá trị của `root`, mạch ZKP sẽ xác thực thành công vòng lặp `root == root`.

### Lời giải

Script `solve.py` thực hiện các bước:
1. Kết nối đến server và khai báo ngựa/chiến thuật.
2. Tại mỗi vòng, nhận thông tin các con ngựa, `Merkle root`, và độ dài đường.
3. Dự đoán con ngựa sẽ về nhất thông qua việc tự mô phỏng cuộc đua với nhiều seed ngẫu nhiên khác nhau và chọn kết quả phổ biến nhất (multi-seed voting).
4. Gửi payload exploit để "nhận" con ngựa về nhất là của mình. Payload sử dụng:
   - `index`: Vị trí của con ngựa dự đoán sẽ thắng.
   - `leaf`: Lấy trực tiếp chuỗi `Merkle root` từ server cung cấp.
   - `path_elements`: `[]` (Mảng rỗng).
   - `path_indices`: `[]` (Mảng rỗng).
5. Lặp lại cho đến khi thắng đủ 50 vòng để lấy cờ.

### Flag

`W1{1-F0rgO7-t0-ch3ck_P4tH-L3ng7h_Of_th3_m3RK13-Tr331dca6}`
