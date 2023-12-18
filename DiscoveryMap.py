import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.image as mpimg
from InteractiveMap import InteractiveMap
import simpleaudio as sa
import os


class DiscoveryMap:
    def __init__(self, fig, ax, dirs, similarities, X):

        ##Layout definitions

        # Map
        w_map = 0.55;
        h_map = 0.7
        P_map = [0.31, 0.5]

        # Prev/next buttons
        w_next_button = .03;
        h_next_button = .05
        x_next_button = 0.15
        x_menu = (P_map[0] + w_map / 2) + (1 - P_map[0] - w_map / 2) / 2
        P_menu = [x_menu, 1 / 3]

        # Name
        w_name = 0.25;
        h_name = 0.05

        # Play/pause buttons
        w_pause_button = .03;
        h_pause_button = .05
        x_pause_button = 0.02;
        y_pause_button = -0.06

        # Similarity
        w_sim = 0.25;
        h_sim = 0.04

        ##File loading
        self.dataset_path = 'data/genres_original'
        self.dirs = dirs
        self.sim = similarities
        self.index = 0

        ##Layout placing
        fig.set_figwidth(10)
        fig.set_figheight(6)
        # Map
        ax.set_position([P_map[0] - w_map / 2, P_map[1] - h_map / 2, w_map, h_map])
        ax.set_xticks([])
        ax.set(xlabel=None)
        ax.set_yticks([])
        ax.set(ylabel=None)
        # ax.axis('off')
        self.ax = ax
        self.X = X

        # Prev/next buttons
        next_ico = mpimg.imread("Icons/next.png")  # [:,:,0]
        prev_ico = mpimg.imread("Icons/prev.png")  # [:,:,0]
        ax_button_next = fig.add_axes(
            [P_menu[0] - w_next_button / 2 + x_next_button, P_menu[1] - h_next_button / 2, w_next_button,
             h_next_button])
        button_next = Button(ax_button_next, '', image=next_ico)
        ax_button_next.axis('off')
        button_next.label.set_fontsize(12)
        button_next.on_clicked(self.next)
        ax_button_prev = fig.add_axes(
            [P_menu[0] - w_next_button / 2 - x_next_button, P_menu[1] - h_next_button / 2, w_next_button,
             h_next_button])
        button_prev = Button(ax_button_prev, '', image=prev_ico)
        ax_button_prev.axis('off')
        button_prev.label.set_fontsize(12)
        button_prev.on_clicked(self.prev)

        # Node highligth
        self.highlight = ax.scatter([], [])

        # Name
        ax_name = fig.add_axes([P_menu[0] - w_name / 2, P_menu[1] - h_name / 2, w_name, h_name])
        plt.ylim((0, 1))
        plt.xlim((0, 1))
        name = self.dirs[self.index]
        self.name_text = ax_name.text(0.5, 0.5, name, ha='center', va='center', fontdict={'size': 14})
        ax_name.set_xticks([])
        ax_name.set_yticks([])
        ax_name.axis('off')

        # Play/pause buttons
        pause_ico = mpimg.imread("Icons\pause.png")  # [:,:,0]
        play_ico = mpimg.imread("Icons\play.png")  # [:,:,0]
        ax_button_pause = fig.add_axes(
            [P_menu[0] - w_pause_button / 2 + x_pause_button, P_menu[1] - h_pause_button / 2 + y_pause_button,
             w_pause_button, h_pause_button])
        button_pause = Button(ax_button_pause, '', image=pause_ico)
        ax_button_pause.axis('off')
        button_pause.on_clicked(self.pause)
        ax_button_play = fig.add_axes(
            [P_menu[0] - w_pause_button / 2 - x_pause_button, P_menu[1] - h_pause_button / 2 + y_pause_button,
             w_pause_button, h_pause_button])
        button_play = Button(ax_button_play, '', image=play_ico)
        ax_button_play.axis('off')
        button_play.on_clicked(self.play)

        # Similarity bar
        ax_sim_bar = fig.add_axes([P_menu[0] - w_sim / 2, P_menu[1] - h_sim / 2 - y_pause_button, w_sim, h_sim])
        ax_sim_bar.set_xticks([])
        ax_sim_bar.set_yticks([])
        plt.ylim((0, 1))
        plt.xlim((0, 1))
        sim = self.sim[self.index]
        if type(sim) == str:
            self.sim_bar = ax_sim_bar.barh(0.5, 0, height=1, color='k')
            self.sim_alt_text = ax_sim_bar.text(0.5, 0.5, "Original", ha='center', va='center', fontdict={'size': 12})
        else:
            self.sim_bar = ax_sim_bar.barh(0.5, sim, height=1, color='k')
            self.sim_alt_text = ax_sim_bar.text(0.5, 0.5, "", ha='center', va='center', fontdict={'size': 12})

        im = InteractiveMap(ax, base_scale=1.4)

        plt.show()

    def play(self, event):
        name = self.dirs[self.index]
        file = self.dir_from_name(name)
        if file:
            sa.stop_all()
            wave_obj = sa.WaveObject.from_wave_file(file)
            play_obj = wave_obj.play()
        # print("Play")

    def pause(self, event):
        sa.stop_all()
        # print("Pause")

    def next(self, event):
        self.index = (self.index + 1) % len(self.dirs)
        self.apply_index_update()
        # print(">>")

    def prev(self, event):
        self.index = (self.index - 1) % len(self.dirs)
        self.apply_index_update()
        # print("<<")

    def dir_from_name(self, name):
        for genre in os.listdir(self.dataset_path):
            genre_path = os.path.join(self.dataset_path, genre)
            for song in os.listdir(genre_path):
                if song == name + ".wav":
                    return os.path.join(genre_path, song)
        return None

    def apply_index_update(self):
        try:
            self.highlight.remove()
        except(ValueError):
            pass

        name = self.dirs[self.index]
        self.name_text.set_text(name)
        sim = self.sim[self.index]
        if type(sim) == str:
            self.sim_bar[0].set_width(0)
            self.sim_alt_text.set_text("Original")
        else:
            self.sim_bar[0].set_width(sim)
            self.sim_alt_text.set_text("")
            X_0 = self.X[self.index]
            self.highlight = self.ax.scatter(X_0[0], X_0[1],
                                             c='none', edgecolors='k', s=150, linewidths=1.5)


if __name__ == "__main__":
    # Test points:
    fig, ax = plt.subplots(figsize=(6, 10))
    X = [[0, 1], [1, 1]]
    ax.scatter(X[0], X[1], c='DarkBlue')

    # Build the map
    DiscoveryMap(fig, ax, dirs=["blues.00001", "blues.00002"], similarities=["s", 0.5], X=X)
