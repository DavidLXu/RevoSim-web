"""Extract only the right-hand RevoBench panels from the supplied comparison recording."""
import argparse
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('source', type=Path)
parser.add_argument('--parts', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
args.parts.mkdir(parents=True, exist_ok=True)
assets = root/'assets'
# x, y, width, height in the original 1568 x 1376 video.
panels = {'hand': (792,124,768,512), 'depth': (792,648,380,354),
          'marker': (1180,648,380,354), 'rgb': (792,1008,380,362),
          'pressure': (1180,1008,380,362)}
encoding = ['-an','-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart']
for name,(x,y,w,h) in panels.items():
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(args.source),
        '-vf',f'crop={w}:{h}:{x}:{y},setsar=1',*encoding,str(args.parts/f'{name}.mp4')],check=True)
# One stream keeps every tactile observation frame-aligned during playback and seeking.
filters = ['[0:v]split=5[h][d][m][r][p]',
    '[h]crop=768:512:792:124,scale=1024:682,pad=1024:728:0:23:color=0x10191e,setsar=1[hand]',
    '[d]crop=380:354:792:648,setsar=1[depth]',
    '[m]crop=380:354:1180:648,setsar=1[marker]',
    '[r]crop=380:362:792:1008,setsar=1[rgb]',
    '[p]crop=380:362:1180:1008,setsar=1[pressure]',
    '[hand][depth][marker][rgb][pressure]xstack=inputs=5:layout=0_0|1040_0|1428_0|1040_366|1428_366:fill=0x10191e[v]']
output=assets/'tactile-contact-right.mp4'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(args.source),
    '-filter_complex',';'.join(filters),'-map','[v]',*encoding,str(output)],check=True)
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss','5','-i',str(output),
    '-frames:v','1','-update','1',str(assets/'tactile-contact-right.jpg')],check=True)
print(output)
