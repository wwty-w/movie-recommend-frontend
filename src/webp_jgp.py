import os
from PIL import Image

# 设置存放图片的文件夹路径
image_folder = r'D:\class_file\2025_9\NLP\Big_Work\short_data\different' 

def convert_webp_to_jpg(folder_path):
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"路径不存在: {folder_path}")
        return

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".webp"):
            # 构建完整的文件路径
            webp_path = os.path.join(folder_path, filename)
            # 构建新的文件名（将 .webp 替换为 .jpg）
            jpg_path = os.path.join(folder_path, filename.lower().replace(".webp", ".jpg"))

            try:
                # 打开图片
                with Image.open(webp_path) as img:
                    # 转换为 RGB 模式 (WebP 可能包含透明层，JPG 不支持，必须转换)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    # 保存为 JPG 格式，quality=95 是质量，可以调整
                    img.save(jpg_path, "JPEG", quality=95)
                    print(f"成功转换: {filename} -> {os.path.basename(jpg_path)}")
                
                # 如果你想转换后删除原 webp 文件，可以取消下面这一行的注释：
                # os.remove(webp_path)

            except Exception as e:
                print(f"转换 {filename} 失败: {e}")

if __name__ == "__main__":
    convert_webp_to_jpg(image_folder)