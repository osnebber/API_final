import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.image as mpimg
from InteractiveMap import InteractiveMap
import simpleaudio as sa
import os

class DiscoveryMap:
    def __init__(self,fig,ax,dirs,similarities):

        ##Layout definitions

        #Map
        w_map=0.45; h_map=0.6
        P_map=[0.25,0.5]

        #Prev/next buttons
        w_next_button=.03; h_next_button=.05
        x_next_button=0.15
        P_menu=[.75,.4]

        #Name
        w_name=0.25; h_name=0.05

        #Play/pause buttons
        w_pause_button=.03; h_pause_button=.05
        x_pause_button=0.02; y_pause_button=-0.1


        ##File loading
        self.dataset_path = 'genres_original'
        self.dirs=dirs
        self.sim=similarities
        self.index=0

        ##Layout placing
        fig.set_figwidth(10)
        fig.set_figheight(6)
        #Map
        ax.set_position([P_map[0]-w_map/2,P_map[1]-h_map/2,w_map,h_map])
        ax.set_xticks([])
        ax.set(xlabel=None)
        ax.set_yticks([])
        ax.set(ylabel=None)
        # ax.axis('off')

        #Prev/next buttons
        next_ico=mpimg.imread("Icons/next.png")#[:,:,0]
        prev_ico=mpimg.imread("Icons/prev.png")#[:,:,0]
        ax_button_next=fig.add_axes([P_menu[0]-w_next_button/2+x_next_button, P_menu[1]-h_next_button/2, w_next_button, h_next_button])    
        button_next = Button(ax_button_next,'',image=next_ico)
        ax_button_next.axis('off')
        button_next.label.set_fontsize(12)
        button_next.on_clicked(self.next)
        ax_button_prev=fig.add_axes([P_menu[0]-w_next_button/2-x_next_button, P_menu[1]-h_next_button/2, w_next_button, h_next_button])    
        button_prev = Button(ax_button_prev,'',image=prev_ico)
        ax_button_prev.axis('off')
        button_prev.label.set_fontsize(12)
        button_prev.on_clicked(self.prev)

        #Name
        ax_name=fig.add_axes([P_menu[0]-w_name/2, P_menu[1]-h_name/2, w_name, h_name])
        plt.ylim((0,1))
        plt.ylim((0,1))
        name=self.dirs[self.index]
        self.name_text=ax_name.text(0.5, 0.5,name, ha='center', va='center', fontdict={'size':14})
        ax_name.set_xticks([])
        ax_name.set_yticks([])
        ax_name.axis('off')

        #Play/pause buttons
        pause_ico=mpimg.imread("Icons\pause.png")#[:,:,0]
        play_ico=mpimg.imread("Icons\play.png")#[:,:,0]
        ax_button_pause=fig.add_axes([P_menu[0]-w_pause_button/2+x_pause_button, P_menu[1]-h_pause_button/2+y_pause_button, w_pause_button, h_pause_button])    
        button_pause = Button(ax_button_pause,'',image=pause_ico)
        ax_button_pause.axis('off')
        button_pause.on_clicked(self.pause)
        ax_button_play=fig.add_axes([P_menu[0]-w_pause_button/2-x_pause_button, P_menu[1]-h_pause_button/2+y_pause_button, w_pause_button, h_pause_button])    
        button_play = Button(ax_button_play,'',image=play_ico)
        ax_button_play.axis('off')
        button_play.on_clicked(self.play)

        im = InteractiveMap(ax,base_scale=1.4)

        plt.show()

    def play(self,event):
        name=self.dirs[self.index]
        file=self.dir_from_name(name)
        if file:
            sa.stop_all()
            wave_obj = sa.WaveObject.from_wave_file(file)
            play_obj = wave_obj.play()
        # print("Play")
    
    def pause(self,event):
        sa.stop_all()
        # print("Pause")

    def next(self,event):
        self.index=(self.index+1) % len(self.dirs)
        name=self.dirs[self.index]
        self.name_text.set_text(name)
        # print(">>")
    
    def prev(self,event):
        self.index=(self.index-1) % len(self.dirs)
        name=self.dirs[self.index]
        self.name_text.set_text(name)
        # print("<<")

    def dir_from_name(self,name):
        for genre in os.listdir(self.dataset_path):
            genre_path = os.path.join(self.dataset_path, genre)
            for song in os.listdir(genre_path):
                if song==name+".wav":
                    return os.path.join(genre_path,song)
        return None
    

if __name__=="__main__":
    #Test points:
    fig,ax=plt.subplots(figsize=(6,10))
    ax.scatter([0,1],[1,1],c='none',edgecolors='k',s=100,linewidths=2)

    #Build the map
    DiscoveryMap(fig,ax,dirs=["blues.00001","blues.00002"],similarities=[0,1])