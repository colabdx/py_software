import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

print("正在制作蒙太奇视频，请耐心等待……")

def select_videos():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    video_paths = []
    for i in range(3):
        file_path = filedialog.askopenfilename(
            title=f"选择第{i+1}个视频文件",
            filetypes=[("视频文件", "*.mp4;*.avi;*.mov")]
        )
        if not file_path:
            print("未选择足够的视频文件！")
            return None
        video_paths.append(file_path)
    
    return video_paths

def create_montage(video_paths):
    # 获取第一个视频的基本参数作为参考
    cap = cv2.VideoCapture(video_paths[0])
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()

    # 创建视频写入对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter('montage.mp4', fourcc, fps, (frame_width, frame_height))

    for video_path in video_paths:
        cap = cv2.VideoCapture(video_path)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # 调整视频大小以适应蒙太奇布局
            frame = cv2.resize(frame, (frame_width // 3, frame_height // 3))
            
            # 创建一个空白画布
            canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
            
            # 将视频片段放置到画布的相应位置
            x = (video_paths.index(video_path) % 3) * (frame_width // 3)
            y = (video_paths.index(video_path) // 3) * (frame_height // 3)
            canvas[y:y+frame_height//3, x:x+frame_width//3] = frame
            
            # 写入蒙太奇视频
            output_video.write(canvas)
        
        cap.release()

    output_video.release()
    print("蒙太奇视频制作完成，文件名为 'montage.mp4'")

if __name__ == "__main__":
    video_paths = select_videos()
    if video_paths:
        create_montage(video_paths)
