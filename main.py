import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import matplotlib.patches as patches
from datetime import datetime, timedelta
import matplotlib.colors as mcolors

# 设置中文字体（如果需要显示中文）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

class TyphoonTracker:
    def __init__(self):
        # 台风数据（英文版）
        self.typhoon_data = {
            "Mangkhut": {
                "name": "Mangkhut",
                "points": [
                    {"lat": 14.5, "lng": 138.2, "pressure": 1002, "wind": 65, "intensity": "TD", "timestamp": "2018-09-07 00:00"},
                    {"lat": 15.2, "lng": 136.8, "pressure": 998, "wind": 75, "intensity": "TS", "timestamp": "2018-09-07 06:00"},
                    {"lat": 16.1, "lng": 135.3, "pressure": 985, "wind": 95, "intensity": "STS", "timestamp": "2018-09-07 12:00"},
                    {"lat": 17.0, "lng": 133.8, "pressure": 970, "wind": 120, "intensity": "TY", "timestamp": "2018-09-07 18:00"},
                    {"lat": 17.9, "lng": 132.3, "pressure": 955, "wind": 140, "intensity": "TY", "timestamp": "2018-09-08 00:00"},
                    {"lat": 18.8, "lng": 130.8, "pressure": 940, "wind": 160, "intensity": "STY", "timestamp": "2018-09-08 06:00"},
                    {"lat": 19.7, "lng": 129.3, "pressure": 920, "wind": 185, "intensity": "SuperTY", "timestamp": "2018-09-08 12:00"},
                    {"lat": 20.6, "lng": 127.8, "pressure": 905, "wind": 205, "intensity": "SuperTY", "timestamp": "2018-09-08 18:00"},
                    {"lat": 21.5, "lng": 126.3, "pressure": 910, "wind": 195, "intensity": "SuperTY", "timestamp": "2018-09-09 00:00"},
                    {"lat": 22.4, "lng": 124.8, "pressure": 925, "wind": 180, "intensity": "STY", "timestamp": "2018-09-09 06:00"}
                ]
            },
            "Haiyan": {
                "name": "Haiyan",
                "points": [
                    {"lat": 6.5, "lng": 155.2, "pressure": 1004, "wind": 55, "intensity": "TD", "timestamp": "2013-11-04 00:00"},
                    {"lat": 7.2, "lng": 153.8, "pressure": 996, "wind": 70, "intensity": "TS", "timestamp": "2013-11-04 06:00"},
                    {"lat": 8.1, "lng": 152.3, "pressure": 980, "wind": 100, "intensity": "STS", "timestamp": "2013-11-04 12:00"},
                    {"lat": 9.0, "lng": 150.8, "pressure": 960, "wind": 130, "intensity": "TY", "timestamp": "2013-11-04 18:00"},
                    {"lat": 9.9, "lng": 149.3, "pressure": 940, "wind": 155, "intensity": "STY", "timestamp": "2013-11-05 00:00"},
                    {"lat": 10.8, "lng": 147.8, "pressure": 920, "wind": 180, "intensity": "SuperTY", "timestamp": "2013-11-05 06:00"},
                    {"lat": 11.7, "lng": 146.3, "pressure": 895, "wind": 215, "intensity": "SuperTY", "timestamp": "2013-11-05 12:00"},
                    {"lat": 12.6, "lng": 144.8, "pressure": 890, "wind": 230, "intensity": "SuperTY", "timestamp": "2013-11-05 18:00"},
                    {"lat": 13.5, "lng": 143.3, "pressure": 895, "wind": 220, "intensity": "SuperTY", "timestamp": "2013-11-06 00:00"},
                    {"lat": 14.4, "lng": 141.8, "pressure": 910, "wind": 200, "intensity": "SuperTY", "timestamp": "2013-11-06 06:00"}
                ]
            },
            "Yutu": {
                "name": "Yutu",
                "points": [
                    {"lat": 12.5, "lng": 147.2, "pressure": 1005, "wind": 60, "intensity": "TD", "timestamp": "2018-10-22 00:00"},
                    {"lat": 13.2, "lng": 145.8, "pressure": 995, "wind": 75, "intensity": "TS", "timestamp": "2018-10-22 06:00"},
                    {"lat": 14.1, "lng": 144.3, "pressure": 980, "wind": 100, "intensity": "STS", "timestamp": "2018-10-22 12:00"},
                    {"lat": 15.0, "lng": 142.8, "pressure": 960, "wind": 125, "intensity": "TY", "timestamp": "2018-10-22 18:00"},
                    {"lat": 15.9, "lng": 141.3, "pressure": 940, "wind": 150, "intensity": "STY", "timestamp": "2018-10-23 00:00"},
                    {"lat": 16.8, "lng": 139.8, "pressure": 920, "wind": 175, "intensity": "SuperTY", "timestamp": "2018-10-23 06:00"},
                    {"lat": 17.7, "lng": 138.3, "pressure": 900, "wind": 195, "intensity": "SuperTY", "timestamp": "2018-10-23 12:00"},
                    {"lat": 18.6, "lng": 136.8, "pressure": 910, "wind": 185, "intensity": "SuperTY", "timestamp": "2018-10-23 18:00"},
                    {"lat": 19.5, "lng": 135.3, "pressure": 925, "wind": 170, "intensity": "STY", "timestamp": "2018-10-24 00:00"},
                    {"lat": 20.4, "lng": 133.8, "pressure": 940, "wind": 155, "intensity": "STY", "timestamp": "2018-10-24 06:00"}
                ]
            }
        }
        
        # 强度颜色映射
        self.intensity_colors = {
            "TD": "#1a9850",
            "TS": "#91cf60",
            "STS": "#d9ef8b",
            "TY": "#fee08b",
            "STY": "#fc8d59",
            "SuperTY": "#d73027"
        }
        
        # 强度完整名称
        self.intensity_names = {
            "TD": "Tropical Depression",
            "TS": "Tropical Storm",
            "STS": "Severe Tropical Storm",
            "TY": "Typhoon",
            "STY": "Severe Typhoon",
            "SuperTY": "Super Typhoon"
        }
        
        # 当前状态
        self.current_typhoon = "Mangkhut"
        self.current_points = []
        self.current_index = 0
        self.is_playing = False
        self.speed = 5
        
        # 创建图形和子图
        self.fig = plt.figure(figsize=(15, 10))
        self.fig.suptitle('Typhoon Track Visualization', fontsize=16, fontweight='bold')
        
        # 创建网格布局
        self.grid = plt.GridSpec(3, 3, figure=self.fig)
        
        # 主地图
        self.ax_map = self.fig.add_subplot(self.grid[:, :2])
        self.ax_map.set_title('Typhoon Track Map')
        self.ax_map.set_xlabel('Longitude')
        self.ax_map.set_ylabel('Latitude')
        
        # 信息面板
        self.ax_info = self.fig.add_subplot(self.grid[0, 2])
        self.ax_info.set_title('Typhoon Information')
        self.ax_info.axis('off')
        
        # 控制面板
        self.ax_controls = self.fig.add_subplot(self.grid[1, 2])
        self.ax_controls.set_title('Controls')
        self.ax_controls.axis('off')
        
        # 图例面板
        self.ax_legend = self.fig.add_subplot(self.grid[2, 2])
        self.ax_legend.set_title('Intensity Legend')
        self.ax_legend.axis('off')
        
        # 初始化图形元素
        self.trajectory_line, = self.ax_map.plot([], [], 'b-', alpha=0.5, linewidth=2)
        self.points_scatter = self.ax_map.scatter([], [], s=50, alpha=0.7)
        self.current_point = self.ax_map.plot([], [], 'ro', markersize=10)[0]
        
        # 初始化文本元素
        self.info_text = self.ax_info.text(0.05, 0.95, '', transform=self.ax_info.transAxes, 
                                          verticalalignment='top', fontsize=10)
        
        # 进度条
        self.progress_bar = patches.Rectangle((0.1, 0.8), 0, 0.1, transform=self.ax_controls.transAxes, 
                                            facecolor='blue', alpha=0.7)
        self.ax_controls.add_patch(self.progress_bar)
        self.progress_text = self.ax_controls.text(0.5, 0.75, '0%', transform=self.ax_controls.transAxes, 
                                                  ha='center', fontsize=12)
        
        # 初始化
        self.load_typhoon_data(self.current_typhoon)
        self.setup_map()
        self.create_legend()
        self.create_controls()
        
        # 设置动画
        self.anim = animation.FuncAnimation(self.fig, self.update, frames=len(self.current_points), 
                                          interval=200, blit=False, repeat=True)
        self.anim.pause()  # 初始状态为暂停
        
    def load_typhoon_data(self, typhoon_name):
        """加载台风数据"""
        self.current_typhoon = typhoon_name
        self.current_points = self.typhoon_data[typhoon_name]["points"]
        self.current_index = 0
        
        # 更新地图范围
        lats = [point["lat"] for point in self.current_points]
        lngs = [point["lng"] for point in self.current_points]
        
        lat_margin = (max(lats) - min(lats)) * 0.2
        lng_margin = (max(lngs) - min(lngs)) * 0.2
        
        self.ax_map.set_xlim(min(lngs) - lng_margin, max(lngs) + lng_margin)
        self.ax_map.set_ylim(min(lats) - lat_margin, max(lats) + lat_margin)
        
    def setup_map(self):
        """设置地图背景"""
        # 添加网格
        self.ax_map.grid(True, alpha=0.3)
        
        # 添加海岸线（简化版）
        coastlines = [
            [(100, 140), (100, 120), (120, 120), (120, 100), (140, 100), (140, 120), (120, 140)],  # 亚洲轮廓
            [(80, 20), (100, 20), (100, 40), (80, 40)]  # 菲律宾轮廓
        ]
        
        for coastline in coastlines:
            lngs, lats = zip(*coastline)
            self.ax_map.plot(lngs, lats, 'k-', linewidth=1, alpha=0.5)
        
        # 添加经纬度标签
        self.ax_map.set_xlabel('Longitude (°E)')
        self.ax_map.set_ylabel('Latitude (°N)')
        
    def create_legend(self):
        """创建图例"""
        y_pos = 0.9
        for intensity, color in self.intensity_colors.items():
            self.ax_legend.add_patch(patches.Rectangle((0.1, y_pos-0.05), 0.1, 0.08, 
                                                     facecolor=color, alpha=0.8))
            self.ax_legend.text(0.25, y_pos, f"{intensity}: {self.intensity_names[intensity]}", 
                              transform=self.ax_legend.transAxes, fontsize=9)
            y_pos -= 0.15
    
    def create_controls(self):
        """创建控制按钮文本"""
        self.ax_controls.text(0.05, 0.6, 'Speed: Medium', transform=self.ax_controls.transAxes, 
                            fontsize=10, color='blue')
        self.ax_controls.text(0.05, 0.4, 'Press Space to Play/Pause', transform=self.ax_controls.transAxes, 
                            fontsize=10, color='green')
        self.ax_controls.text(0.05, 0.2, 'Press R to Reset', transform=self.ax_controls.transAxes, 
                            fontsize=10, color='red')
    
    def update_typhoon_info(self):
        """更新台风信息"""
        if self.current_index < len(self.current_points):
            point = self.current_points[self.current_index]
            
            info_str = (
                f"Name: {self.typhoon_data[self.current_typhoon]['name']}\n\n"
                f"Time: {point['timestamp']}\n\n"
                f"Intensity: {self.intensity_names[point['intensity']]}\n\n"
                f"Pressure: {point['pressure']} hPa\n\n"
                f"Wind Speed: {point['wind']} km/h\n\n"
                f"Position: {point['lat']:.1f}°N, {point['lng']:.1f}°E"
            )
            
            # 计算移动速度和方向（简化版）
            if self.current_index > 0:
                prev_point = self.current_points[self.current_index - 1]
                distance = self.calculate_distance(prev_point["lat"], prev_point["lng"], 
                                                 point["lat"], point["lng"])
                speed = round(distance / 6)  # 假设每6小时一个数据点
                direction = self.calculate_direction(prev_point["lat"], prev_point["lng"], 
                                                   point["lat"], point["lng"])
                info_str += f"\n\nMovement: {speed} km/h, {direction}"
            
            self.info_text.set_text(info_str)
    
    def calculate_distance(self, lat1, lng1, lat2, lng2):
        """计算两点间距离（简化版）"""
        d_lat = (lat2 - lat1) * 111  # 纬度每度约111km
        d_lng = (lng2 - lng1) * 111 * np.cos((lat1 + lat2) / 2 * np.pi / 180)
        return np.sqrt(d_lat**2 + d_lng**2)
    
    def calculate_direction(self, lat1, lng1, lat2, lng2):
        """计算移动方向"""
        d_lat = lat2 - lat1
        d_lng = lng2 - lng1
        
        if abs(d_lng) < 0.001:
            return "North" if d_lat > 0 else "South"
        
        angle = np.arctan2(d_lat, d_lng) * 180 / np.pi
        
        if -22.5 <= angle < 22.5:
            return "East"
        elif 22.5 <= angle < 67.5:
            return "Northeast"
        elif 67.5 <= angle < 112.5:
            return "North"
        elif 112.5 <= angle < 157.5:
            return "Northwest"
        elif angle >= 157.5 or angle < -157.5:
            return "West"
        elif -157.5 <= angle < -112.5:
            return "Southwest"
        elif -112.5 <= angle < -67.5:
            return "South"
        elif -67.5 <= angle < -22.5:
            return "Southeast"
        
        return "Unknown"
    
    def update(self, frame):
        """更新动画帧"""
        self.current_index = frame
        
        # 更新轨迹线
        lats = [point["lat"] for point in self.current_points[:frame+1]]
        lngs = [point["lng"] for point in self.current_points[:frame+1]]
        self.trajectory_line.set_data(lngs, lats)
        
        # 更新所有点
        all_lats = [point["lat"] for point in self.current_points]
        all_lngs = [point["lng"] for point in self.current_points]
        colors = [self.intensity_colors[point["intensity"]] for point in self.current_points]
        
        # 清除并重新创建散点图
        self.points_scatter.remove()
        self.points_scatter = self.ax_map.scatter(all_lngs, all_lats, c=colors, s=50, alpha=0.7)
        
        # 更新当前点
        if frame < len(self.current_points):
            current_point = self.current_points[frame]
            self.current_point.set_data([current_point["lng"]], [current_point["lat"]])
            
            # 添加脉冲动画效果
            pulse_circle = Circle((current_point["lng"], current_point["lat"]), 
                                 radius=0.5, fill=False, 
                                 edgecolor=self.intensity_colors[current_point["intensity"]], 
                                 linewidth=2, alpha=0.7)
            self.ax_map.add_patch(pulse_circle)
            
            # 移除之前的脉冲圆圈
            for patch in self.ax_map.patches[1:]:  # 跳过第一个（如果有的话）
                if isinstance(patch, Circle) and patch.get_fill() == False:
                    patch.remove()
        
        # 更新信息
        self.update_typhoon_info()
        
        # 更新进度条
        progress = (frame / (len(self.current_points) - 1)) * 100 if len(self.current_points) > 1 else 0
        self.progress_bar.set_width(0.8 * progress / 100)
        self.progress_text.set_text(f'{progress:.1f}%')
        
        return self.trajectory_line, self.points_scatter, self.current_point, self.info_text, self.progress_bar, self.progress_text
    
    def toggle_animation(self, event):
        """切换动画播放状态"""
        if event.key == ' ':
            if self.anim.event_source:
                if self.is_playing:
                    self.anim.event_source.stop()
                    self.is_playing = False
                else:
                    self.anim.event_source.start()
                    self.is_playing = True
    
    def reset_animation(self, event):
        """重置动画"""
        if event.key == 'r' or event.key == 'R':
            self.anim.event_source.stop()
            self.current_index = 0
            self.is_playing = False
            self.update(0)
            self.fig.canvas.draw()
    
    def change_typhoon(self, typhoon_name):
        """切换台风"""
        self.anim.event_source.stop()
        self.load_typhoon_data(typhoon_name)
        self.current_index = 0
        self.is_playing = False
        self.update(0)
        self.fig.canvas.draw()

# 创建并显示动画
def main():
    tracker = TyphoonTracker()
    
    # 添加键盘事件监听
    tracker.fig.canvas.mpl_connect('key_press_event', tracker.toggle_animation)
    tracker.fig.canvas.mpl_connect('key_press_event', tracker.reset_animation)
    
    # 添加台风选择按钮（简化版）
    ax_mangkhut = tracker.fig.add_axes([0.05, 0.02, 0.1, 0.04])
    btn_mangkhut = plt.Button(ax_mangkhut, 'Mangkhut')
    btn_mangkhut.on_clicked(lambda x: tracker.change_typhoon("Mangkhut"))
    
    ax_haiyan = tracker.fig.add_axes([0.17, 0.02, 0.1, 0.04])
    btn_haiyan = plt.Button(ax_haiyan, 'Haiyan')
    btn_haiyan.on_clicked(lambda x: tracker.change_typhoon("Haiyan"))
    
    ax_yutu = tracker.fig.add_axes([0.29, 0.02, 0.1, 0.04])
    btn_yutu = plt.Button(ax_yutu, 'Yutu')
    btn_yutu.on_clicked(lambda x: tracker.change_typhoon("Yutu"))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()