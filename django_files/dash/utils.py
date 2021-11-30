import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph
    
def get_plot(x, yt, yh, ym, yvi, yIR, yUV):
    plt.switch_backend('AGG')
    
    fig = plt.figure(figsize=(12,18))
    plt.style.use('seaborn')
    fig.patch.set_alpha(0.0)
    
    plt.subplots_adjust(top=1.0)

    ax1 = plt.subplot(611)
    #ax1.set_title('Temperature')
    ax1.set_ylabel('Temp $^\circ$C', fontsize=14)
    plt.plot(x, yt, color = 'green')
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax1.xaxis.set_major_locator(MaxNLocator(24))
    ax1.patch.set_facecolor('#E8EBE4')

    ax2 = plt.subplot(612)
    #ax2.set_title('Humidity')
    ax2.set_ylabel('Humid %', fontsize=14)
    plt.plot(x, yh)
    plt.setp(ax2.get_xticklabels(), visible=False)
    ax2.xaxis.set_major_locator(MaxNLocator(24))
    ax2.patch.set_facecolor('#E8EBE4')

    ax3 = plt.subplot(613)
    #ax3.set_title('Soil Moisture')
    ax3.set_ylabel('Soil Moist %', fontsize=14)
    plt.plot(x, ym, color = 'brown')
    plt.setp(ax3.get_xticklabels(), visible=False)
    ax3.xaxis.set_major_locator(MaxNLocator(24))
    ax3.patch.set_facecolor('#E8EBE4')

    ax4 = plt.subplot(614)
    #ax4.set_title('Visible Light')
    ax4.set_ylabel('Vis Light lm', fontsize=14)
    plt.plot(x, yvi, color = 'yellow')
    plt.setp(ax4.get_xticklabels(), visible=False)
    ax4.xaxis.set_major_locator(MaxNLocator(24))
    ax4.patch.set_facecolor('#E8EBE4')    

    ax5 = plt.subplot(615)
    #ax5.set_title('IR Light')
    ax5.set_ylabel('IR Light lm', fontsize=14)
    plt.plot(x, yIR, color = 'red')
    plt.setp(ax5.get_xticklabels(), visible=False)
    ax5.xaxis.set_major_locator(MaxNLocator(24))
    ax5.patch.set_facecolor('#E8EBE4') 

    ax6 = plt.subplot(616, sharex=ax1)
    #ax6.set_title('UV Light')
    ax6.set_ylabel('UV Light UVI', fontsize=14)
    plt.plot(x, yUV, color = 'violet')
    plt.xticks(x, rotation='45')
    ax6.xaxis.set_major_locator(MaxNLocator(24))
    ax6.patch.set_facecolor('#E8EBE4')
    plt.subplots_adjust(bottom=0.15)
    

    graph= get_graph()
    plt.tight_layout()

    return graph

