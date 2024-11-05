import os
import pandas as pd
import glob
from datetime import date
import numpy as np
from sklearn import preprocessing

from mplsoccer import Pitch, VerticalPitch, PyPizza, Radar, grid
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.font_manager as fm
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as patches
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)

from PIL import Image
from tempfile import NamedTemporaryFile
import urllib
import os

github_url = 'https://github.com/google/fonts/blob/main/ofl/poppins/Poppins-Bold.ttf'
url = github_url + '?raw=true'

response = urllib.request.urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()

bold = fm.FontProperties(fname=f.name)

github_url = 'https://github.com/google/fonts/blob/main/ofl/poppins/Poppins-Regular.ttf'
url = github_url + '?raw=true'

response = urllib.request.urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()

reg = fm.FontProperties(fname=f.name)

github_url = 'https://github.com/google/fonts/blob/main/ofl/poppins/Poppins-Italic.ttf'
url = github_url + '?raw=true'

response = urllib.request.urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()

ita = fm.FontProperties(fname=f.name)

path_eff = [path_effects.Stroke(linewidth=2, foreground='#ffffff'),
            path_effects.Normal()]

posdict = {'gk':{'position':'Goalkeeper',
                 'metrics':['Name','Long Goal Kick Ratio','Pass Accuracy','Cross Claim',
                            'Keeper - Sweeper','Save','Save Ratio','Penalty Save']},
           'cb':{'position':'Center Back',
                 'metrics':['Name','Non-penalty goals','Shots',
                            'Passes to final 3rd','Progressive passes','Long passes','Pass accuracy',
                            'Tackles','Intercepts','Recoveries','Blocks','Clearances','Aerial duel won ratio','Defensive duel won ratio']},
           'fb':{'position':'Fullback',
                 'metrics':['Name','Non-penalty goals','Non-penalty xG','Shots','Chances created','Assists',
                            'Passes-to-box','Through passes','Passes to final 3rd','Progressive passes','Pass accuracy','Successful dribbles','Successful crosses','Offensive duel won ratio',
                            'Tackles','Intercepts','Recoveries','Blocks','Clearances','Aerial duel won ratio','Defensive duel won ratio']},
           'cm':{'position':'Midfielder',
                 'metrics':['Name','Non-penalty goals','Non-penalty xG','NPxG/Shot','Shots','Shot on target ratio','Chances created','Assists',
                            'Passes-to-box','Through passes','Passes to final 3rd','Progressive passes','Long passes','Pass accuracy','Successful dribbles','Offensive duel won ratio',
                            'Tackles','Intercepts','Recoveries','Clearances','Defensive duel won ratio']},
           'cam/w':{'position':'Attacking 10/Winger',
                    'metrics':['Name','Non-penalty goals','Non-penalty xG','NPxG/Shot','Shots','Shot on target ratio','Conversion ratio','Chances created','Assists',
                               'Passes-to-box','Through passes','Passes to final 3rd','Progressive passes','Pass accuracy','Successful dribbles','Offensive duel won ratio',
                               'Tackles','Intercepts','Recoveries','Defensive duel won ratio']},
           'fw':{'position':'Forward',
                 'metrics':['Name','Non-penalty goals','Non-penalty xG','NPxG/Shot','Shots','Shot on target ratio','Conversion ratio','Chances created','Assists',
                            'Passes-to-box','Through passes','Progressive passes','Pass accuracy','Successful dribbles','Offensive duel won ratio',
                            'Tackles','Intercepts','Recoveries','Aerial duel won ratio','Defensive duel won ratio']}}

def proses_tl(data):
  dfx = data.copy()
  dfx = dfx[dfx['Act Zone'].notna()]
  dfx = dfx[dfx['Pas Zone'].notna()]
  dfx = dfx[['Act Name', 'Action', 'Act Zone', 'Pas Zone']]
  dfx = dfx[(dfx['Action']=='passing')].reset_index(drop=True)

  vv = dfx[dfx['Pas Zone'].str.contains("6B|6C|6D")]
  vv = vv[vv['Act Zone'].str.contains("1|2|3|4|5|6A|6E")].reset_index(drop=True)
  vv = vv[['Act Name','Action']].rename(columns={'Act Name':'Name','Action':'Passes-to-box'})
  vv = vv.groupby(['Name'], as_index=False).count()

  yy = dfx[dfx['Pas Zone'].str.contains("5|6")]
  yy = yy[yy['Act Zone'].str.contains("1|2|3|4")].reset_index(drop=True)
  yy = yy[['Act Name','Action']].rename(columns={'Act Name':'Name','Action':'Passes to final 3rd'})
  yy = yy.groupby(['Name'], as_index=False).count()

  dz = pd.merge(vv, yy, on='Name', how='outer')
  dz.fillna(0, inplace=True)

  return dz

metrik = ['Name','Team','MoP','Non-penalty goals','Non-penalty xG','NPxG/Shot','Shots','Shot on target ratio','Conversion ratio','Chances created','Assists',
          'Passes-to-box','Through passes','Passes to final 3rd','Progressive passes','Long passes','Pass accuracy','Successful crosses',
          'Successful dribbles','Offensive duel won ratio','Tackles','Intercepts','Recoveries','Blocks','Clearances','Aerial duel won ratio',
          'Defensive duel won ratio']

jamet = ['Name','Team','MoP','Non-penalty goals','Shots','Chances created','Assists','Through passes','Progressive passes',
         'Long passes','Successful crosses','Successful dribbles','Tackles','Intercepts','Recoveries','Blocks','Clearances',
         'Total Pass','Aerial Duels','Offensive Duel','Offensive Duel - Won','Defensive Duel','Defensive Duel - Won','Goal',
         'Shot on','Pass','Aerial Won','Penalty']

def get_sum90(report, tl, xg, db, min):
  df = report.copy()
  df2 = tl.copy()
  db = db.copy()

  dxg = xg.copy()
  dxg = dxg[['Name','xG']]
  dxg = dxg.groupby(['Name'], as_index=False).sum()

  df['Non-penalty goals'] = df['Goal']
  df['Shots'] = df['Shot on']+df['Shot off']+df['Shot Blocked']
  df['Chances created'] = df['Create Chance']
  df['Assists'] = df['Assist']
  df['Through passes'] = df['Pass - Through Pass']
  df['Progressive passes'] = df['Pass - Progressive Pass']
  df['Long passes'] = df['Pass - Long Ball']
  df['Successful crosses'] = df['Cross']
  df['Successful dribbles'] = df['Dribble']
  df['Tackles'] = df['Tackle']
  df['Intercepts'] = df['Intercept']
  df['Recoveries'] = df['Recovery']
  df['Blocks'] = df['Block']+df['Block Cross']
  df['Clearances'] = df['Clearance']

  df['Total Pass'] = df['Pass']+df['Pass Fail']
  df['Aerial Duels'] = df['Aerial Won']+df['Aerial Lost']
  df['Offensive Duel - Won'] = df['Offensive Duel - Won']+df['Fouled']+df['Dribble']
  df['Offensive Duel - Lost'] = df['Offensive Duel - Lost']+df['Loose Ball - Tackle']+df['Dribble Fail']
  df['Defensive Duel - Won'] = df['Defensive Duel - Won']+df['Tackle']
  df['Defensive Duel - Lost'] = df['Defensive Duel - Lost']+df['Foul']+df['Dribbled Past']
  df['Offensive Duel'] = df['Offensive Duel - Won']+df['Offensive Duel - Lost']
  df['Defensive Duel'] = df['Defensive Duel - Won']+df['Defensive Duel - Lost']
  df['Penalty'] = df['Penalty Goal']-df['Penalty Missed']

  df_data = df[jamet]
  df_sum = df_data.groupby(['Name','Team'], as_index=False).sum()
  df_sum = pd.merge(df_sum, dxg, on='Name', how='outer')

  df_sum['Non-penalty xG'] = round(df_sum['xG']-(df_sum['Penalty']*0.593469436750998),2)
  df_sum['NPxG/Shot'] = round(df_sum['Non-penalty xG']/(df_sum['Shots']-df_sum['Penalty']),2)
  df_sum['Conversion ratio'] = round(df_sum['Goal']/df_sum['Shots'],2)
  df_sum['Shot on target ratio'] = round(df_sum['Shot on']/df_sum['Shots'],2)
  df_sum['Pass accuracy'] = round(df_sum['Pass']/df_sum['Total Pass'],2)
  df_sum['Aerial duel won ratio'] = round(df_sum['Aerial Won']/df_sum['Aerial Duels'],2)
  df_sum['Offensive duel won ratio'] = round(df_sum['Offensive Duel - Won']/df_sum['Offensive Duel'],2)
  df_sum['Defensive duel won ratio'] = round(df_sum['Defensive Duel - Won']/df_sum['Defensive Duel'],2)

  temp = proses_tl(df2)
  df_sum = pd.merge(df_sum, temp, on='Name', how='outer')

  df_sum.replace([np.inf, -np.inf], 0, inplace=True)
  df_sum.fillna(0, inplace=True)

  temp = df_sum.drop(['Name','Team'], axis=1)

  def p90_Calculator(variable_value):
    p90_value = round((((variable_value/temp['MoP']))*90),2)
    return p90_value
  p90 = temp.apply(p90_Calculator)

  p90['Name'] = df_sum['Name']
  p90['Team'] = df_sum['Team']
  p90['MoP'] = df_sum['MoP']
  p90['NPxG/Shot'] = df_sum['NPxG/Shot']
  p90['Conversion ratio'] = df_sum['Conversion ratio']
  p90['Shot on target tatio'] = df_sum['Shot on target ratio']
  p90['Pass accuracy'] = df_sum['Pass accuracy']
  p90['Aerial duel won ratio'] = df_sum['Aerial duel won ratio']
  p90['Offensive duel won ratio'] = df_sum['Offensive duel won ratio']
  p90['Defensive duel won ratio'] = df_sum['Defensive duel won ratio']

  p90 = p90[metrik]
  p90['Name'] = p90['Name'].str.strip()

  pos = db[['Name','Position']]
  data_full = pd.merge(p90, pos, on='Name', how='left')
  data_full = data_full.loc[(data_full['MoP']>=min)].reset_index(drop=True)

  return data_full, df_sum

def get_pct(data):
  data_full = data.copy()
  df4 = data_full.groupby('Position', as_index=False)
  midfielder = df4.get_group('Midfielder')
  goalkeeper = df4.get_group('Goalkeeper')
  forward = df4.get_group('Forward')
  att_10 = df4.get_group('Attacking 10')
  center_back = df4.get_group('Center Back')
  fullback = df4.get_group('Fullback')
  winger = df4.get_group('Winger')

  #calculating the average stats per position
  #winger
  temp = winger.copy()
  winger = winger.drop(['Name','Position','Team'], axis=1)
  winger.loc['mean'] = round((winger.mean()),2)
  winger['Name'] = temp['Name']
  winger['Position'] = temp['Position']
  winger['Team'] = temp['Team']
  values1 = {"Name": 'Average W', "Position": 'Winger', "Team": 'League Average'}
  winger = winger.fillna(value=values1)

  #fb
  temp = fullback.copy()
  fullback = fullback.drop(['Name','Position','Team'], axis=1)
  fullback.loc['mean'] = round((fullback.mean()),2)
  fullback['Name'] = temp['Name']
  fullback['Position'] = temp['Position']
  fullback['Team'] = temp['Team']
  values2 = {"Name": 'Average FB', "Position": 'Fullback', "Team": 'League Average'}
  fullback = fullback.fillna(value=values2)

  #cb
  temp = center_back.copy()
  center_back = center_back.drop(['Name','Position','Team'], axis=1)
  center_back.loc['mean'] = round((center_back.mean()),2)
  center_back['Name'] = temp['Name']
  center_back['Position'] = temp['Position']
  center_back['Team'] = temp['Team']
  values3 = {"Name": 'Average CB', "Position": 'Center Back', "Team": 'League Average'}
  center_back = center_back.fillna(value=values3)

  #cam
  temp = att_10.copy()
  att_10 = att_10.drop(['Name','Position','Team'], axis=1)
  att_10.loc['mean'] = round((att_10.mean()),2)
  att_10['Name'] = temp['Name']
  att_10['Position'] = temp['Position']
  att_10['Team'] = temp['Team']
  values4 = {"Name": 'Average CAM', "Position": 'Attacking 10', "Team": 'League Average'}
  att_10 = att_10.fillna(value=values4)

  #forward
  temp = forward.copy()
  forward = forward.drop(['Name','Position','Team'], axis=1)
  forward.loc['mean'] = round((forward.mean()),2)
  forward['Name'] = temp['Name']
  forward['Position'] = temp['Position']
  forward['Team'] = temp['Team']
  values5 = {"Name": 'Average FW', "Position": 'Forward', "Team": 'League Average'}
  forward = forward.fillna(value=values5)

  #gk
  temp = goalkeeper.copy()
  goalkeeper = goalkeeper.drop(['Name','Position','Team',], axis=1)
  goalkeeper.loc['mean'] = round((goalkeeper.mean()),2)
  goalkeeper['Name'] = temp['Name']
  goalkeeper['Position'] = temp['Position']
  goalkeeper['Team'] = temp['Team']
  values6 = {"Name": 'Average GK', "Position": 'Goalkeeper', "Team": 'League Average'}
  goalkeeper = goalkeeper.fillna(value=values6)

  #cm
  temp = midfielder.copy()
  midfielder = midfielder.drop(['Name','Position','Team'], axis=1)
  midfielder.loc['mean'] = round((midfielder.mean()),2)
  midfielder['Name'] = temp['Name']
  midfielder['Position'] = temp['Position']
  midfielder['Team'] = temp['Team']
  values7 = {"Name": 'Average CM', "Position": 'Midfielder', "Team": 'League Average'}
  midfielder = midfielder.fillna(value=values7)

  #percentile rank
  rank_cm = round(((midfielder.rank(pct=True))*100),0).astype(int)
  rank_gk = round(((goalkeeper.rank(pct=True))*100),0).astype(int)
  rank_fw = round(((forward.rank(pct=True))*100),0).astype(int)
  rank_cam = round(((att_10.rank(pct=True))*100),0).astype(int)
  rank_cb = round(((center_back.rank(pct=True))*100),0).astype(int)
  rank_fb = round(((fullback.rank(pct=True))*100),0).astype(int)
  rank_w = round(((winger.rank(pct=True))*100),0).astype(int)

  #adding Name and Position back
  rank_cm['Name'] = midfielder['Name']
  rank_gk['Name'] = goalkeeper['Name']
  rank_fw['Name'] = forward['Name']
  rank_cam['Name'] = att_10['Name']
  rank_cb['Name'] = center_back['Name']
  rank_fb['Name'] = fullback['Name']
  rank_w['Name'] = winger['Name']

  rank_cm['Position'] = midfielder['Position']
  rank_gk['Position'] = goalkeeper['Position']
  rank_fw['Position'] = forward['Position']
  rank_cam['Position'] = att_10['Position']
  rank_cb['Position'] = center_back['Position']
  rank_fb['Position'] = fullback['Position']
  rank_w['Position'] = winger['Position']

  rank_cm['Team'] = midfielder['Team']
  rank_gk['Team'] = goalkeeper['Team']
  rank_fw['Team'] = forward['Team']
  rank_cam['Team'] = att_10['Team']
  rank_cb['Team'] = center_back['Team']
  rank_fb['Team'] = fullback['Team']
  rank_w['Team'] = winger['Team']

  rank_cm['MoP'] = midfielder['MoP']
  rank_gk['MoP'] = goalkeeper['MoP']
  rank_fw['MoP'] = forward['MoP']
  rank_cam['MoP'] = att_10['MoP']
  rank_cb['MoP'] = center_back['MoP']
  rank_fb['MoP'] = fullback['MoP']
  rank_w['MoP'] = winger['MoP']

  rank_liga = pd.concat([rank_cm, rank_gk, rank_fw, rank_cam, rank_cb, rank_fb, rank_w]).reset_index(drop=True)
  rank_liga['MoP'] = rank_liga['MoP'].astype(int)

  return rank_liga

def beli_pizza(komp, pos, klub, name, data, mins):
  df = data.copy()
  df = df[df['Position']==pos]

  #DATA
  if (pos=='Forward'):
    temp = df[posdict['fw']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==name) | (temp['Name']=='Average FW')].reset_index(drop=True)

    slice_colors = ['#e900ff']*8 + ['#faeb2c']*6 + ['#74ee15']*5

  elif (pos=='Winger') or (pos=='Attacking 10'):
    temp = df[posdict['cam/w']['metrics']].reset_index(drop=True)
    if (pos=='Winger'):
      temp = temp[(temp['Name']==name) | (temp['Name']=='Average W')].reset_index(drop=True)
    else:
      temp = temp[(temp['Name']==name) | (temp['Name']=='Average CAM')].reset_index(drop=True)

    slice_colors = ['#e900ff']*8 + ['#faeb2c']*7 + ['#74ee15']*4

  elif (pos=='Midfielder'):
    temp = df[posdict['cm']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==name) | (temp['Name']=='Average CM')].reset_index(drop=True)

    slice_colors = ['#e900ff']*7 + ['#faeb2c']*8 + ['#74ee15']*5

  elif (pos=='Fullback'):
    temp = df[posdict['fb']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==name) | (temp['Name']=='Average FB')].reset_index(drop=True)

    slice_colors = ['#e900ff']*5 + ['#faeb2c']*8 + ['#74ee15']*7

  elif (pos=='Center Back'):
    temp = df[posdict['cb']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==name) | (temp['Name']=='Average CB')].reset_index(drop=True)

    slice_colors = ['#e900ff']*2 + ['#faeb2c']*4 + ['#74ee15']*7

  elif (pos=='Goalkeeper'):
    temp = df[posdict['gk']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==name) | (temp['Name']=='Average GK')].reset_index(drop=True)

    slice_colors = ['#e900ff']*2 + ['#74ee15']*5

  #temp = temp.drop(['Team'], axis=1)

  avg_player = temp[temp['Name'].str.contains('Average')]
  av_name = avg_player['Name'].values[0]
  params = list(temp.columns)
  params = params[1:]

  a_values = []
  b_values = []

  for x in range(len(temp['Name'])):
    if temp['Name'][x] == name:
      a_values = temp.iloc[x].values.tolist()
    if temp['Name'][x] == av_name:
      b_values = temp.iloc[x].values.tolist()

  a_values = a_values[1:]
  b_values = b_values[1:]

  values = [a_values,b_values]
  maxmin = pd.DataFrame({'param':params,'value':a_values,'average':b_values})
  for index, value in enumerate(params):
    if value == 'Progressive passes':
      params[index] = 'Progressive\npasses'
    elif value == 'long passes':
      params[index] = 'Long\npasses'
    elif value == 'Pass accuracy':
      params[index] = 'Pass\naccuracy'
    elif value == 'Successful crosses':
      params[index] = 'Successful\ncrosses'
    elif value == 'Successful dribbles':
      params[index] = 'Successful\ndribbles'
    elif value == 'Offensive duel won ratio':
      params[index] = 'Offensive duel\nwon ratio'
    elif value == 'Defensive duel won ratio':
      params[index] = 'Defensive duel\nwon ratio'
    elif value == 'Aerial duel won ratio':
      params[index] = 'Aerial\nduel won\nratio'
    elif value == 'Passes to final 3rd':
      params[index] = 'Passes to\nfinal 3rd'
    elif value == 'Through passes':
      params[index] = 'Through\npasses'
    elif value == 'Non-penalty goals':
      params[index] = 'Non-penalty\ngoals'
    elif value == 'Shot on target ratio':
      params[index] = 'Shot on\ntarget ratio'
    elif value == 'Conversion ratio':
      params[index] = 'Conversion\nratio'
    elif value == 'Chances created':
      params[index] = 'Chances\ncreated'

  #PLOT
  # set figure size
  fig = plt.figure(figsize=(10,10))

  # plot polar axis
  ax = plt.subplot(111, polar=True)
  ax.set_theta_direction(-1)
  ax.set_theta_zero_location('N')

  # Set the grid and spine off
  fig.patch.set_facecolor('#FFFFFF')
  ax.set_facecolor('#FFFFFF')
  ax.spines['polar'].set_visible(False)
  plt.axis('off')

  # Add line in 20, 40, 60, 80
  x2 = np.linspace(0, 2*np.pi, 50)
  annot_x = [20 + x*20 for x in range(0,4)]
  for z in annot_x:
    ax.plot(x2, [z]*50, color='#000000', lw=1, ls='--', alpha=0.15, zorder=4)
  ax.plot(x2, [100]*50, color='#000000', lw=2, zorder=10, alpha=0.5, ls=(0, (5, 1)))
  # Set the coordinates limits
  upperLimit = 100
  lowerLimit = 0

  # Compute max and min in the dataset
  max = maxmin['value'].max()

  # Let's compute heights: they are a conversion of each item value in those new coordinates
  # In our example, 0 in the dataset will be converted to the lowerLimit (10)
  # The maximum will be converted to the upperLimit (100)
  slope = (max-lowerLimit)/max
  heights = slope*maxmin['value'] + lowerLimit
  avg_heights = slope*maxmin['average'] + lowerLimit
  va_heights = maxmin['value']*0 + 90
  #shadow = df.Value*0 + 100

  # Compute the width of each bar. In total we have 2*Pi = 360°
  width = 2*np.pi/len(a_values)

  # Compute the angle each bar is centered on:
  indexes = list(range(1, len(a_values)+1))
  angles = [element*width for element in indexes]

  # Draw bars
  bars = ax.bar(x=angles, height=heights, width=width, bottom=lowerLimit, linewidth=2, edgecolor='#FFFFFF', zorder=3, alpha=1, color=slice_colors)
  #bars = ax.bar(x=angles, height=shadow, width=width, bottom=lowerLimit, linewidth=2, edgecolor='#000000', zorder=2, alpha=0.15, color=slice_colors)

  # Draw scatter plots for the averages and values
  scas_av = ax.scatter(x=angles, y=avg_heights, s=150, c=slice_colors, zorder=5, ec='#000000')
  #scas_va = ax.scatter(x=angles, y=va_heights, s=350, c='#000000',
  #                     zorder=4, marker='s', lw=0.5, ec='#ffffff')

  # Draw vertical lines for reference
  ax.vlines(angles, 0, 100, color='#000000', ls='--', zorder=4, alpha=0.35)

  # Add labels
  for bar, angle, height, label, value in zip(bars,angles, heights, params, a_values):
    # Labels are rotated. Rotation must be specified in degrees :(
    rotation = np.rad2deg((np.pi/2)-angle)
    # Flip some labels upside down
    if (angle <= np.pi/2) or (angle >= (np.pi/2)+np.pi):
        rotation = rotation+270
    else:
        rotation = rotation+90

    # Finally add the labels and values
    ax.text(x=angle, y=110, s=label, color='#000000', ha='center',
            va='center', rotation=rotation, rotation_mode='anchor',
            fontproperties=reg)
    ax.text(x=angle, y=90, s=value, color='#000000', zorder=11, va='center',
            ha='center', fontproperties=bold, bbox=dict(facecolor='#FFFFFF', edgecolor='#000000',
                                                        boxstyle='circle, pad=0.5'))

  fig.text(0.325, 0.9325, "Attacking                                Possession                            Defending",
           fontproperties=reg, size=10, color='#000000', va='center')

  fig.patches.extend([plt.Circle((0.305, 0.935), 0.01, fill=True, color='#e900ff',
                                    transform=fig.transFigure, figure=fig),
                      plt.Circle((0.490, 0.935), 0.01, fill=True, color='#faeb2c',
                                    transform=fig.transFigure, figure=fig),
                      plt.Circle((0.668, 0.935), 0.01, fill=True, color='#74ee15',
                                    transform=fig.transFigure, figure=fig),
                      plt.Circle((0.15, 0.0425), 0.01, fill=True, color='#000000',
                                 transform=fig.transFigure, figure=fig)])

  fig.text(0.515, 0.985,name + ' - ' + klub, fontproperties=bold, size=18,
           ha='center', color='#000000')
  fig.text(0.515, 0.963, 'Percentile Rank vs League Average '+pos,
           fontproperties=reg, size=11, ha='center', color='#000000')

  fig.text(0.17, 0.04, 'League Average', fontproperties=reg, size=10, color='#000000', va='center')

  CREDIT_1 = 'Data: Lapangbola'
  CREDIT_2 = komp+' | Season 2024/25 | Min. '+str(mins)+' mins played'

  fig.text(0.515, 0.025, f'{CREDIT_1}\n{CREDIT_2}', fontproperties=reg,
           size=11, color='#000000', ha='center')
  
  DC_to_FC = ax.transData.transform
  FC_to_NFC = fig.transFigure.inverted().transform
  DC_to_NFC = lambda x: FC_to_NFC(DC_to_FC(x))

  logo_ax = fig.add_axes([0.73, 0.015, 0.15, 0.05], anchor = "NE")
  club_icon = Image.open('./data/logo2.png')
  logo_ax.imshow(club_icon)
  logo_ax.axis("off")

  fig.savefig('pizza.jpg', dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')

  return fig

def player_dist(komp, pos, klub, player, data, mins):
  att = data[data['Position']==pos].reset_index(drop=True)
  if (pos=='Forward'):
    att = att[posdict['fw']['metrics']].reset_index(drop=True)
  elif (pos=='Winger') or (pos=='Attacking 10'):
    att = att[posdict['cam/w']['metrics']].reset_index(drop=True)
  elif (pos=='Midfielder'):
    att = att[posdict['cm']['metrics']].reset_index(drop=True)
  elif (pos=='Fullback'):
    att = att[posdict['fb']['metrics']].reset_index(drop=True)
  elif (pos=='Center Back'):
    att = att[posdict['cb']['metrics']].reset_index(drop=True)
  elif (pos=='Goalkeeper'):
    att = att[posdict['gk']['metrics']].reset_index(drop=True)
  params = list(att.columns)
  params = params[1:]
  ngroups = len(params)
  bandwidth = 1
  samsize = len(att)

  fig, axs = plt.subplots(nrows=ngroups, ncols=1, figsize=(8, 16), dpi=500)
  fig.patch.set_facecolor('#FFFFFF')
  axs = axs.flatten() # needed to access each individual axis

  at = ['Non-penalty goals','Non-penalty xG','NPxG/Shot','Shots','Shot on target ratio','Conversion ratio','Chances created','Assists']
  po = ['Passes-to-box','Through passes','Passes to final 3rd','Progressive passes','Long passes','Pass accuracy','Successful crosses',
        'Successful dribbles','Offensive duel won ratio']
  de = ['Tackles','Intercepts','Recoveries','Blocks','Clearances','Aerial duel won ratio','Defensive duel won ratio']

  # iterate over axes
  for i, param in enumerate(params):
    axs[i].set_facecolor('#FFFFFF')
    my_kde = sns.kdeplot(att[param], bw_adjust=bandwidth, ax=axs[i], lw=0)
    axs[i].set_ylim(bottom=0)
    line = my_kde.lines[0]
    x, y = line.get_data()

    axs[i].fill_between(x, y, color='grey', alpha=0.25, lw=0)
    if param in at:
      axs[i].fill_between(x, y, where=x<=(att[att['Name']==player][param].reset_index(drop=True)[0]),
                          color='#e900ff', alpha=0.75, lw=0)
      axs[i].hlines(y=0, xmin=axs[i].get_xlim()[0], xmax=att[att['Name']==player][param].reset_index(drop=True)[0],
                    linewidth=3, color='#e900ff')
    elif param in po:
      axs[i].fill_between(x, y, where=x<=(att[att['Name']==player][param].reset_index(drop=True)[0]),
                          color='#faeb2c', alpha=0.75, lw=0)
      axs[i].hlines(y=0, xmin=axs[i].get_xlim()[0], xmax=att[att['Name']==player][param].reset_index(drop=True)[0],
                    linewidth=3, color='#faeb2c')
    else:
      axs[i].fill_between(x, y, where=x<=(att[att['Name']==player][param].reset_index(drop=True)[0]),
                          color='#74ee15', alpha=0.75, lw=0)
      axs[i].hlines(y=0, xmin=axs[i].get_xlim()[0], xmax=att[att['Name']==player][param].reset_index(drop=True)[0],
                    linewidth=3, color='#74ee15')
    axs[i].hlines(y=0, xmin=att[att['Name']==player][param].reset_index(drop=True)[0], xmax=axs[i].get_xlim()[1],
                  linewidth=3, color='grey', alpha=0.5)
    axs[i].set_axis_off()
    axs[i].annotate(param, (0.05, 0.2), xycoords='axes fraction', fontproperties=bold, size=10, ha='right')
    axs[i].annotate(str(att[param].min()), (0.05, 0.1), xycoords='axes fraction', fontproperties=reg, size=8, ha='left', alpha=0.5)
    axs[i].annotate(str(att[param].max()), (0.85, 0.1), xycoords='axes fraction', fontproperties=reg,
                    size=8, ha='left', alpha=0.5)
    axs[i].annotate(str(att[att['Name']==player][param].reset_index(drop=True)[0]), (0.9, 0.25),
                    xycoords='axes fraction', fontproperties=bold, size=12, ha='left', color='#000000')

    axs[i].axvline(att[param].mean(), color='#000000', linestyle='--', alpha=0.65)
    axs[i].scatter(att[att['Name']==player][param].reset_index(drop=True)[0], axs[i].get_ylim()[0],
                   color='#000000', s=100, marker='^', zorder=2)
    
    fig.text(0.865, 0.925, player + ' - ' + klub, fontproperties=bold, size=14,
             ha='right', color='#000000')
    fig.text(0.865, 0.915, 'vs Liga 1\'s '+pos+'s, '+str(mins)+'+ mins | Sample size: '+str(samsize)+' players', fontproperties=reg, size=8,
             ha='right', color='#000000')
    
    fig.text(0.84, 0.875, 'Per 90\'\nNumber', ha='center', fontsize=9, fontproperties=reg)
    fig.text(0.865, 0.1, 'Dashed lines (--) indicate mean', fontproperties=ita, size=8,
             ha='right', color='#000000', alpha=0.05)
    
  DC_to_FC = axs[i].transData.transform
  FC_to_NFC = fig.transFigure.inverted().transform
  DC_to_NFC = lambda x: FC_to_NFC(DC_to_FC(x))

  logo_ax = fig.add_axes([0.725, 0.877, 0.15, 0.05], anchor = "E")
  club_icon = Image.open('./data/logo2.png')
  logo_ax.imshow(club_icon)
  logo_ax.axis("off")
    
  fig.savefig('dist.jpg', dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    
  return fig
