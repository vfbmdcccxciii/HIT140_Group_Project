"""Shared sampling and course-aligned two-sample inference for Max's two tasks."""
from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / 'outputs'
RANDOM_SEED = 2026

def mean_confidence_interval(values):
    x = np.asarray(values, dtype=float)
    if len(x)<2 or not np.isfinite(x).all():
        raise ValueError('At least two finite observations required')
    margin = stats.t.ppf(.975,len(x)-1)*x.std(ddof=1)/math.sqrt(len(x))
    return x.mean()-margin,x.mean()+margin

def compare_means(first,second):
    a,b = np.asarray(first,dtype=float),np.asarray(second,dtype=float)
    mean_confidence_interval(a)
    mean_confidence_interval(b)
    se = math.sqrt(a.var(ddof=1)/len(a)+b.var(ddof=1)/len(b))
    if se == 0: raise ValueError('Zero standard error')
    difference = a.mean()-b.mean()
    t = difference/se
    df = min(len(a)-1,len(b)-1)
    p = 2*stats.t.sf(abs(t),df)
    margin = stats.t.ppf(.975,df)*se
    welch = stats.ttest_ind(a,b,equal_var=False)
    return dict(mean_difference_MF_minus_FW=difference,standard_error=se,t_statistic=t,
        degrees_of_freedom=df,p_value_two_sided=p,difference_ci_95_lower=difference-margin,
        difference_ci_95_upper=difference+margin,welch_df=welch.df,welch_p_value=welch.pvalue,
        alpha=.05,decision='Reject H0' if p<.05 else 'Fail to reject H0')

def random_sample_by_group(data,n):
    if n<30: raise ValueError('Use at least 30 observations per group')
    if data.duplicated(['player','team','position']).any(): raise ValueError('Duplicate keys')
    return pd.concat([data.loc[data.position==g].sample(n=n,replace=False,random_state=2026+i)
                      for i,g in enumerate(['MF','FW'])],ignore_index=True)

def run_task(data,name,metric,label,n):
    OUTPUT_DIR.mkdir(exist_ok=True)
    if not np.isfinite(data[metric]).all(): raise ValueError('Nonfinite focal metric')
    sample = random_sample_by_group(data,n)
    rows=[]
    for i,g in enumerate(['MF','FW']):
        x=sample.loc[sample.position==g,metric]
        lo,hi=mean_confidence_interval(x)
        q1,q3=x.quantile([.25,.75])
        rows.append(dict(group=['Midfielders','Forwards'][i],eligible_n=int((data.position==g).sum()),
            n=len(x),seed=2026+i,mean=x.mean(),median=x.median(),standard_deviation=x.std(ddof=1),
            minimum=x.min(),maximum=x.max(),q1=q1,q3=q3,skewness=x.skew(),
            iqr_outliers=int(((x<q1-1.5*(q3-q1))|(x>q3+1.5*(q3-q1))).sum()),
            ci_95_lower=lo,ci_95_upper=hi))
    summary=pd.DataFrame(rows)
    result=pd.DataFrame([compare_means(sample.loc[sample.position=='MF',metric],sample.loc[sample.position=='FW',metric])])
    sample.to_csv(OUTPUT_DIR/f'{name}_sample.csv',index=False)
    summary.to_csv(OUTPUT_DIR/f'{name}_descriptive_and_ci.csv',index=False)
    result.to_csv(OUTPUT_DIR/f'{name}_t_test.csv',index=False)
    data.groupby('position')[metric].agg(['count','mean','median','std','min','max']).to_csv(OUTPUT_DIR/f'{name}_eligible_frame_summary.csv')
    sns.set_theme(style='whitegrid',font_scale=1.2)
    colors=['#087F8C','#D87532']
    fig,ax=plt.subplots(figsize=(9,4.5))
    for i,row in summary.iterrows():
        ax.errorbar(row['mean'],1-i,xerr=[[row['mean']-row.ci_95_lower],[row.ci_95_upper-row['mean']]],fmt='o',markersize=10,capsize=7,color=colors[i],linewidth=2.5)
        ax.annotate(f"{row['mean']:.2f}  [{row.ci_95_lower:.2f}, {row.ci_95_upper:.2f}]",(row['mean'],1-i),xytext=(0,22),textcoords='offset points',ha='center',fontsize=16,color=colors[i])
    span=summary.ci_95_upper.max()-summary.ci_95_lower.min()
    ax.set_xlim(summary.ci_95_lower.min()-.35*span,summary.ci_95_upper.max()+.35*span)
    ax.set_yticks([1,0],['Midfielders','Forwards'])
    ax.set_ylim(-.55,1.6)
    ax.set_xlabel(label)
    ax.set_title('Sample means and 95% t confidence intervals',fontsize=16,pad=18)
    ax.grid(axis='y',visible=False)
    sns.despine(ax=ax,left=True)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR/f'{name}_means_ci.png',dpi=180)
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.6))
    sns.boxplot(data=sample,x='position',y=metric,order=['MF','FW'],color='#E5ECEF',ax=ax)
    sns.swarmplot(data=sample,x='position',y=metric,order=['MF','FW'],color='#223442',size=4,ax=ax)
    ax.set_xticks([0,1],['Midfielders','Forwards'])
    ax.set_xlabel('')
    ax.set_ylabel(label)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR/f'{name}_distribution.png',dpi=180)
    plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(9,4),sharex=True,sharey=True)
    bins=np.linspace(sample[metric].min(),sample[metric].max(),9)
    for ax,g,title,color in zip(axes,['MF','FW'],['Midfielders','Forwards'],colors):
        ax.hist(sample.loc[sample.position==g,metric],bins=bins,color=color,edgecolor='white')
        ax.set_title(title)
        ax.set_xlabel(label,fontsize=11)
    axes[0].set_ylabel('Players')
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR/f'{name}_histogram.png',dpi=180)
    plt.close(fig)
    print(name)
    print(summary.to_string(index=False))
    print(result.to_string(index=False))
    return summary,result
