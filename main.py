import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import matplotlib.colors as mcolors
from datetime import datetime
import warnings

# 忽略libpng警告
warnings.filterwarnings("ignore", category=UserWarning, message="libpng warning: iCCP")

class Arrow3D(FancyArrowPatch):
    """Custom 3D arrow class for direction indicators"""
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

class TyphoonTracker3D:
    def __init__(self):
        # Typhoon data (English version)
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
        
        # Intensity color mapping
        self.intensity_colors = {
            "TD": "#1a9850",
            "TS": "#91cf60",
            "STS": "#d9ef8b",
            "TY": "#fee08b",
            "STY": "#fc8d59",
            "SuperTY": "#d73027"
        }
        
        # Intensity full names
        self.intensity_names = {
            "TD": "Tropical Depression",
            "TS": "Tropical Storm",
            "STS": "Severe Tropical Storm",
            "TY": "Typhoon",
            "STY": "Severe Typhoon",
            "SuperTY": "Super Typhoon"
        }
        
        # Current state
        self.current_typhoon = "Mangkhut"
        self.current_points = []
        self.current_index = 0
        self.is_playing = False
        self.speed = 5
        
        # Create figure with better layout
        self.fig = plt.figure(figsize=(16, 12))
        self.fig.suptitle('3D Typhoon Track Visualization', fontsize=16, fontweight='bold')
        
        # Create subplots with adjusted layout
        self.ax_3d = self.fig.add_subplot(231, projection='3d')
        self.ax_3d.set_title('3D Typhoon Track', pad=10)
        
        self.ax_map = self.fig.add_subplot(232)
        self.ax_map.set_title('2D Map View', pad=10)
        
        self.ax_pressure = self.fig.add_subplot(233)
        self.ax_pressure.set_title('Pressure Profile', pad=10)
        
        self.ax_wind = self.fig.add_subplot(234)
        self.ax_wind.set_title('Wind Speed Profile', pad=10)
        
        self.ax_info = self.fig.add_subplot(235)
        self.ax_info.set_title('Typhoon Information', pad=10)
        self.ax_info.axis('off')
        
        self.ax_legend = self.fig.add_subplot(236)
        self.ax_legend.set_title('Intensity Legend', pad=10)
        self.ax_legend.axis('off')
        
        # Initialize visualization elements
        self.setup_plots()
        
        # Load initial data
        self.load_typhoon_data(self.current_typhoon)
        
        # Animation control
        self.anim = None
        
        # Adjust layout to prevent tight_layout warnings
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, wspace=0.3, hspace=0.4)
        
    def setup_plots(self):
        """Setup all plot elements"""
        self.setup_3d_plot()
        self.setup_2d_map()
        self.setup_profiles()
        self.create_legend()
        
    def load_typhoon_data(self, typhoon_name):
        """Load typhoon data"""
        self.current_typhoon = typhoon_name
        self.current_points = self.typhoon_data[typhoon_name]["points"]
        self.current_index = 0
        
        # Calculate data arrays
        self.lats = np.array([point["lat"] for point in self.current_points])
        self.lngs = np.array([point["lng"] for point in self.current_points])
        self.pressures = np.array([point["pressure"] for point in self.current_points])
        self.winds = np.array([point["wind"] for point in self.current_points])
        self.intensities = [point["intensity"] for point in self.current_points]
        self.colors = [self.intensity_colors[intensity] for intensity in self.intensities]
        
        # Update plot limits
        self.update_plot_limits()
        
    def setup_3d_plot(self):
        """Setup 3D visualization"""
        self.ax_3d.set_xlabel('Longitude (°E)')
        self.ax_3d.set_ylabel('Latitude (°N)')
        self.ax_3d.set_zlabel('Pressure (hPa)')
        self.ax_3d.invert_zaxis()  # Lower pressure (stronger storm) appears higher
        self.ax_3d.grid(True, alpha=0.3)
        
    def setup_2d_map(self):
        """Setup 2D map view"""
        self.ax_map.set_xlabel('Longitude (°E)')
        self.ax_map.set_ylabel('Latitude (°N)')
        self.ax_map.grid(True, alpha=0.3)
        self.add_coastlines()
        
    def add_coastlines(self):
        """Add simplified coastlines to 2D map"""
        # Asia coastline (simplified)
        asia_lons = [100, 100, 120, 120, 140, 140, 120, 100]
        asia_lats = [10, 30, 30, 40, 40, 20, 20, 10]
        self.ax_map.plot(asia_lons, asia_lats, 'k-', linewidth=1, alpha=0.5)
        
        # Philippines coastline (simplified)
        ph_lons = [117, 122, 126, 126, 122, 117]
        ph_lats = [5, 5, 15, 20, 20, 15]
        self.ax_map.plot(ph_lons, ph_lats, 'k-', linewidth=1, alpha=0.5)
        
    def setup_profiles(self):
        """Setup pressure and wind profile plots"""
        self.ax_pressure.set_xlabel('Time Step')
        self.ax_pressure.set_ylabel('Pressure (hPa)')
        self.ax_pressure.grid(True, alpha=0.3)
        self.ax_pressure.invert_yaxis()
        
        self.ax_wind.set_xlabel('Time Step')
        self.ax_wind.set_ylabel('Wind Speed (km/h)')
        self.ax_wind.grid(True, alpha=0.3)
        
    def create_legend(self):
        """Create intensity legend"""
        y_pos = 0.9
        for intensity, color in self.intensity_colors.items():
            self.ax_legend.add_patch(plt.Rectangle((0.1, y_pos-0.05), 0.1, 0.08, 
                                                 facecolor=color, alpha=0.8, transform=self.ax_legend.transAxes))
            self.ax_legend.text(0.25, y_pos, f"{intensity}: {self.intensity_names[intensity]}", 
                              transform=self.ax_legend.transAxes, fontsize=8)
            y_pos -= 0.15
            
    def update_plot_limits(self):
        """Update plot limits based on current data"""
        # Add margins to limits
        lat_margin = max((self.lats.max() - self.lats.min()) * 0.2, 2)
        lon_margin = max((self.lngs.max() - self.lngs.min()) * 0.2, 2)
        pressure_margin = max((self.pressures.max() - self.pressures.min()) * 0.2, 20)
        
        # 3D plot limits
        self.ax_3d.set_xlim(self.lngs.min() - lon_margin, self.lngs.max() + lon_margin)
        self.ax_3d.set_ylim(self.lats.min() - lat_margin, self.lats.max() + lat_margin)
        self.ax_3d.set_zlim(self.pressures.min() - pressure_margin, self.pressures.max() + pressure_margin)
        
        # 2D map limits
        self.ax_map.set_xlim(self.lngs.min() - lon_margin, self.lngs.max() + lon_margin)
        self.ax_map.set_ylim(self.lats.min() - lat_margin, self.lats.max() + lat_margin)
        
        # Profile limits
        time_points = len(self.current_points)
        if time_points > 1:
            self.ax_pressure.set_xlim(-0.5, time_points - 0.5)
            self.ax_wind.set_xlim(-0.5, time_points - 0.5)
        else:
            self.ax_pressure.set_xlim(-0.5, 0.5)
            self.ax_wind.set_xlim(-0.5, 0.5)
            
        self.ax_pressure.set_ylim(self.pressures.max() + 50, self.pressures.min() - 50)
        self.ax_wind.set_ylim(0, max(self.winds.max() * 1.2, 100))
    
    def update_typhoon_info(self, frame):
        """Update typhoon information display"""
        if frame < len(self.current_points):
            point = self.current_points[frame]
            
            info_text = (
                f"Typhoon: {self.typhoon_data[self.current_typhoon]['name']}\n"
                f"Time: {point['timestamp']}\n"
                f"Intensity: {self.intensity_names[point['intensity']]}\n"
                f"Pressure: {point['pressure']} hPa\n"
                f"Wind Speed: {point['wind']} km/h\n"
                f"Position: {point['lat']:.1f}°N, {point['lng']:.1f}°E"
            )
            
            # Calculate movement direction
            if frame > 0:
                prev_point = self.current_points[frame - 1]
                direction = self.calculate_direction(prev_point["lat"], prev_point["lng"], 
                                                   point["lat"], point["lng"])
                info_text += f"\nMovement: {direction}"
            
            # Clear and display info
            self.ax_info.clear()
            self.ax_info.axis('off')
            self.ax_info.set_title('Typhoon Information', pad=10)
            self.ax_info.text(0.05, 0.95, info_text, transform=self.ax_info.transAxes, 
                            verticalalignment='top', fontsize=9, fontfamily='monospace')
    
    def calculate_direction(self, lat1, lng1, lat2, lng2):
        """Calculate movement direction"""
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
    
    def update_visualization(self, frame):
        """Update all visualization elements for current frame"""
        try:
            # Clear all plots
            self.ax_3d.clear()
            self.ax_map.clear()
            self.ax_pressure.clear()
            self.ax_wind.clear()
            
            # Re-setup plots
            self.setup_3d_plot()
            self.setup_2d_map()
            self.setup_profiles()
            self.add_coastlines()
            
            if frame < len(self.current_points):
                # Current point data
                current_lat = self.lats[frame]
                current_lng = self.lngs[frame]
                current_pressure = self.pressures[frame]
                current_wind = self.winds[frame]
                current_color = self.colors[frame]
                
                # 3D trajectory
                self.ax_3d.plot(self.lngs[:frame+1], self.lats[:frame+1], self.pressures[:frame+1], 
                              'b-', alpha=0.5, linewidth=2)
                
                # 3D scatter points
                for i in range(frame + 1):
                    self.ax_3d.scatter(self.lngs[i], self.lats[i], self.pressures[i],
                                     c=self.colors[i], s=50, alpha=0.7)
                
                # Current position in 3D
                self.ax_3d.scatter([current_lng], [current_lat], [current_pressure], 
                                 c=[current_color], s=200, alpha=1.0, edgecolors='white', linewidth=2)
                
                # 2D map trajectory
                self.ax_map.plot(self.lngs[:frame+1], self.lats[:frame+1], 'b-', alpha=0.5, linewidth=2)
                
                # 2D scatter points
                for i in range(frame + 1):
                    self.ax_map.scatter(self.lngs[i], self.lats[i], c=self.colors[i], s=30, alpha=0.7)
                
                # Current position in 2D
                self.ax_map.scatter([current_lng], [current_lat], c=[current_color], s=100, alpha=1.0, 
                                  edgecolors='white', linewidth=2)
                
                # Pulse effect in 2D
                pulse_circle = plt.Circle((current_lng, current_lat), 1.5, fill=False, 
                                        edgecolor=current_color, linewidth=2, alpha=0.7)
                self.ax_map.add_patch(pulse_circle)
                
                # Pressure profile
                if frame >= 1:
                    self.ax_pressure.plot(range(frame+1), self.pressures[:frame+1], 'b-', linewidth=2)
                    for i in range(frame + 1):
                        self.ax_pressure.scatter(i, self.pressures[i], c=self.colors[i], s=50)
                
                # Current pressure point
                self.ax_pressure.scatter(frame, current_pressure, c=[current_color], s=100, 
                                       edgecolors='black', linewidth=2)
                
                # Wind speed profile
                if frame >= 1:
                    self.ax_wind.plot(range(frame+1), self.winds[:frame+1], 'g-', linewidth=2)
                    for i in range(frame + 1):
                        self.ax_wind.scatter(i, self.winds[i], c=self.colors[i], s=50)
                
                # Current wind point
                self.ax_wind.scatter(frame, current_wind, c=[current_color], s=100, 
                                   edgecolors='black', linewidth=2)
                
                # Update information and titles
                self.update_typhoon_info(frame)
                self.ax_3d.set_title(f'3D Typhoon Track\n{self.intensity_names[self.intensities[frame]]}', pad=10)
                self.ax_map.set_title(f'2D Map View\nFrame: {frame+1}/{len(self.current_points)}', pad=10)
                self.ax_pressure.set_title('Pressure Profile', pad=10)
                self.ax_wind.set_title('Wind Speed Profile', pad=10)
                
            # Update plot limits
            self.update_plot_limits()
            
        except Exception as e:
            print(f"Error in update_visualization: {e}")
            
        return []
    
    def start_animation(self):
        """Start the animation"""
        if self.anim is None:
            self.anim = animation.FuncAnimation(
                self.fig, 
                self.update_visualization, 
                frames=len(self.current_points), 
                interval=800,  # Slower interval for better viewing
                blit=False, 
                repeat=True
            )
            self.is_playing = True
        
        plt.show()
    
    def toggle_animation(self):
        """Toggle animation play/pause"""
        if self.anim:
            if self.is_playing:
                self.anim.event_source.stop()
                self.is_playing = False
            else:
                self.anim.event_source.start()
                self.is_playing = True
    
    def change_typhoon(self, typhoon_name):
        """Change current typhoon"""
        self.load_typhoon_data(typhoon_name)
        if self.anim:
            self.anim.event_source.stop()
            self.anim = None
        self.current_index = 0
        self.is_playing = False
        
        # Redraw with new data
        self.update_visualization(0)
        plt.draw()

def main():
    """Main function to run the 3D typhoon tracker"""
    # Set matplotlib backend to avoid GUI issues
    plt.switch_backend('TkAgg')
    
    tracker = TyphoonTracker3D()
    
    # Create control buttons with better positioning
    button_y = 0.02
    button_height = 0.04
    button_width = 0.12
    button_spacing = 0.13
    
    ax_mangkhut = plt.axes([0.05, button_y, button_width, button_height])
    btn_mangkhut = plt.Button(ax_mangkhut, 'Mangkhut')
    btn_mangkhut.on_clicked(lambda x: tracker.change_typhoon("Mangkhut"))
    
    ax_haiyan = plt.axes([0.05 + button_spacing, button_y, button_width, button_height])
    btn_haiyan = plt.Button(ax_haiyan, 'Haiyan')
    btn_haiyan.on_clicked(lambda x: tracker.change_typhoon("Haiyan"))
    
    ax_yutu = plt.axes([0.05 + 2*button_spacing, button_y, button_width, button_height])
    btn_yutu = plt.Button(ax_yutu, 'Yutu')
    btn_yutu.on_clicked(lambda x: tracker.change_typhoon("Yutu"))
    
    ax_play = plt.axes([0.05 + 3*button_spacing, button_y, button_width, button_height])
    btn_play = plt.Button(ax_play, 'Play/Pause')
    btn_play.on_clicked(lambda x: tracker.toggle_animation())
    
    ax_start = plt.axes([0.05 + 4*button_spacing, button_y, button_width, button_height])
    btn_start = plt.Button(ax_start, 'Start Animation')
    btn_start.on_clicked(lambda x: tracker.start_animation())
    
    # Add keyboard controls
    def on_key(event):
        if event.key == ' ':
            tracker.toggle_animation()
        elif event.key == 'r' or event.key == 'R':
            tracker.change_typhoon(tracker.current_typhoon)
    
    tracker.fig.canvas.mpl_connect('key_press_event', on_key)
    
    # Add instructions
    tracker.fig.text(0.05, 0.97, "Controls: Space=Play/Pause, R=Reset", 
                    fontsize=10, style='italic')
    
    # Initial display
    tracker.update_visualization(0)
    
    print("3D Typhoon Tracker Started!")
    print("Controls:")
    print("- Press Space to play/pause animation")
    print("- Press R to reset animation")
    print("- Use buttons to switch between typhoons")
    
    plt.show()

if __name__ == "__main__":
    main()