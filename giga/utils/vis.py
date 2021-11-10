import os
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np


TECH_COLORS = {#'fiber':'Black',
               'WISP':'lawngreen',
               'Satellite':'Orange',
               '2G':'Yellow',
               '3G':'green',
               '4G':'red'}

BIZ_COLORS = {True:'lawngreen', False:'black'}

def plot_school_locations(filename, data, country):
    #Location of Schools
    plt.figure()
    country.plot(color='#b8c9d9')
    plt.scatter(data['Lon'], data['Lat'], s=1, c=data['Distance to Nearest Fiber'], cmap='hot')
    plt.colorbar()
    plt.axis('off')
    plt.title('School locations,\ncoded by distance to nearest fiber (km)')
    plt.savefig(filename)

def plot_school_locations_with_tech(filename, data, country):
    plt.figure()
    country.plot(color='#b8c9d9')
    plt.scatter(data['Lon'], data['Lat'],
                s=1,c=[TECH_COLORS[i] for i in data['technology']])
    plt.title('School locations, color coded by connection type')
    blackdot = mlines.Line2D([], [], color='Black', marker='.', linestyle='None',
                              markersize=4, label='Fiber')
    purpledot = mlines.Line2D([], [], color='Orange', marker='.', linestyle='None',
                              markersize=4, label='Satellite')
    orangedot = mlines.Line2D([], [], color='lawngreen', marker='.', linestyle='None',
                              markersize=4, label='WISP')
    yellowdot = mlines.Line2D([], [], color='yellow', marker='.', linestyle='None',
                              markersize=4, label='2G')
    greendot = mlines.Line2D([], [], color='green', marker='.', linestyle='None',
                              markersize=4, label='3G')
    reddot = mlines.Line2D([], [], color='red', marker='.', linestyle='None',
                              markersize=4, label='4G')
    plt.legend(handles=[blackdot,orangedot,purpledot, yellowdot, greendot, reddot])
    plt.axis('off')
    plt.savefig(filename)

def plot_distance_to_fiber(filename, data):
    bins = np.arange(0,100,10)
    xlabels = bins[1:].astype(str)
    xlabels[-1] += '+'
    plt.figure()
    plt.hist(np.clip(data['Distance to Nearest Fiber'], bins[0], bins[-1]), bins=50, color='#607c8e')
    plt.ylabel('School Count')
    plt.xlabel('Distance to nearest fiber (km)')
    plt.title('Distribution of school proximity to nearest fiber (km)')
    plt.tight_layout()
    plt.savefig(filename)

def plot_bandwidths(filename, data):
    bins = np.arange(0,100,10)
    plt.figure()
    plt.hist(np.clip(data['bandwidth'], bins[0], bins[-1]), bins=50, color='#607c8e')
    plt.ylabel('School Count')
    plt.xlabel('Bandwidth (Mbps)')
    plt.title('Distribution of school bandwidth requirements')
    plt.tight_layout()
    plt.savefig(filename)

def plot_tech_choices(filename, data):
    plt.figure()
    plt.hist(data['technology'], rwidth=0.99, color='#607c8e')
    plt.xlabel('Technology')
    plt.ylabel('Counts')
    plt.title('Distribution of Technologies')
    plt.savefig(filename)

def plot_school_by_biz(filename, data, country):
    plt.figure()
    country.plot(color='#b8c9d9')
    plt.scatter(data['Lon'], data['Lat'], s=1, c=[BIZ_COLORS[i] for i in data['explore_business_model']])
    plt.title('School locations, color coded by ability to sustain a business model')
    greendot = mlines.Line2D([], [], color='lawngreen', marker='.', linestyle='None',
                              markersize=4, label='Explore Biz Model')
    blackdot = mlines.Line2D([], [], color='black', marker='.', linestyle='None',
                              markersize=4, label='No Likely Biz Model')
    plt.legend(handles=[greendot, blackdot])
    plt.axis('off')
    plt.savefig(filename)

def plot_all(plot_dir, data, country):
    plot_school_locations(os.path.join(plot_dir, 'school_locations.pdf'), data, country)
    plot_school_locations_with_tech(os.path.join(plot_dir, 'tech_locations.pdf'), data, country)
    plot_school_by_biz(os.path.join(plot_dir, 'business_models.pdf'), data, country)
    plot_distance_to_fiber(os.path.join(plot_dir, 'fiber_distance.pdf'), data)
    plot_bandwidths(os.path.join(plot_dir, 'bandwidths.pdf'), data)
    plot_tech_choices(os.path.join(plot_dir, 'technologies.pdf'), data)
