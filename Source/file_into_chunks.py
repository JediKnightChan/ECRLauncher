import os.path


def split_file_into_chunks(fp_, chunk_size=2_000_000_000, piece_size=10_000_000):
    with open(fp_, "rb") as f:
        current_chunk = 0
        current_bytes_read = 0

        # Delete chunk 0 if exists
        if os.path.exists(fp_ + f".chunk.{current_chunk}"):
            os.remove(fp_ + f".chunk.{current_chunk}")

        while True:
            piece = f.read(piece_size)
            if not piece:
                break
            current_bytes_read += piece_size

            # Appending piece
            with open(fp_ + f".chunk.{current_chunk}", "ab") as f2:
                f2.write(piece)

            # Check if next will be large
            if current_bytes_read + piece_size > chunk_size:
                current_chunk += 1
                print(f"New chunk is {current_chunk}")
                current_bytes_read = 0

                # Delete chunk i > 0 if exists
                if os.path.exists(fp_ + f".chunk.{current_chunk}"):
                    os.remove(fp_ + f".chunk.{current_chunk}")


if __name__ == '__main__':
    root_dir = "C:/Users/JediKnight/Documents/Unreal Projects/ECRPackagedShipping/"
    end_path = "dev_1.0.1/dev_1.0.1.zip"
    fp = os.path.join(root_dir, end_path)

    split_file_into_chunks(fp)
