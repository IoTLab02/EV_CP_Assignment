# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.chdir(r"C:\Phd\CUDA test\Test\test 1\V2V_charging_service\code\EV_assignment")

def plot_varyingEV(csv_file, q):
    data = pd.read_csv(csv_file)
    
    markers = {
        'random_elemination': 'o',
        'PCG': 's',
        'PCD': 'D'
    }
    
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='Total EV', y='execution time', marker=marker, label=method)
    plt.xlabel('Total EV', fontsize=18)
    plt.ylabel('Execution Time (ms)', fontsize=18)
    plt.title('Execution Time', fontsize=18)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.grid(True)
    plt.savefig(f'execution_time_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    # Plot 2
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='Total EV', y='Total charge transferred in-net', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=18)
    plt.ylabel('Total Charge Transferred In-net (kWh)', fontsize=18)
    plt.title('In-net Charge Transfer', fontsize=18)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.grid(True)
    plt.savefig(f'In-net_Charge_Transfer_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    ## Plot 3
    # data2 = data[data['Method'] !='random_elemination']
    data['total SLA missed'] = data['Total SLA breach'] + data['unmatched EV']
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        # if method=='random_elemination':
        #     continue
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='Total EV', y='total SLA missed', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=18)
    plt.ylabel('Missed SLA', fontsize=18)
    plt.title('SLA Analysis', fontsize=18)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.grid(True)
    plt.savefig(f'missed_SLA_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    ## Plot 4 & 5
    # Filter the data for the required methods
    pcg_data = data[data['Method'] == 'PCG']
    pcd_data = data[data['Method'] == 'PCD']
    
    palette = sns.color_palette("mako", 4)
    
    # Prepare the data for bar plotting
    plot_data = pd.DataFrame({
        'Total EV': pd.concat([pcg_data['Total EV'], pcg_data['Total EV'], pcd_data['Total EV'], pcd_data['Total EV']]),
        'EV Charged': pd.concat([pcg_data['Total EV charged in-net'], pcg_data['Total EV charged par-net'], 
                                 pcd_data['Total EV charged in-net'], pcd_data['Total EV charged par-net']]),
        'Category': ['PCG In-net'] * len(pcg_data) + ['PCG par-net'] * len(pcg_data) + 
                    ['PCD In-net'] * len(pcd_data) + ['PCD par-net'] * len(pcd_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='Total EV', y='EV Charged', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=18)
    plt.ylabel('EV Charged', fontsize=18)
    plt.title('EV Assignments', fontsize=18)
    plt.legend(title='Category', fontsize=16, title_fontsize=18, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.grid(True)
    plt.savefig(f'EV_Assignments_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    # plot charge transferred
    palette = sns.color_palette("rocket", 4)
    plot_data = pd.DataFrame({
        'Total EV': pd.concat([pcg_data['Total EV'], pcg_data['Total EV'], pcd_data['Total EV'], pcd_data['Total EV']]),
        'EV Charged': pd.concat([pcg_data['Total charge transferred in-net'], pcg_data['Total charge transferred par-net'], 
                                 pcd_data['Total charge transferred in-net'], pcd_data['Total charge transferred par-net']]),
        'Category': ['PCG In-net'] * len(pcg_data) + ['PCG par-net'] * len(pcg_data) + 
                    ['PCD In-net'] * len(pcd_data) + ['PCD par-net'] * len(pcd_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='Total EV', y='EV Charged', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=18)
    plt.ylabel('Total charge transferred (kWh)', fontsize=18)
    plt.title('Transferred Charge', fontsize=18)
    plt.legend(title='Category', fontsize=16, title_fontsize=18, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.grid(True)
    plt.savefig(f'Transferred_Charge_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    
    
def plot_varyingQ(csv_file, n_ev):
    data = pd.read_csv(csv_file)
    xtick_values = data['CP Queue'].unique()
    
    markers = {
        'random_elemination': 'o',
        'PCG': 's',
        'PCD': 'D'
    }
    
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='CP Queue', y='execution time', marker=marker, label=method)
    plt.xlabel(r'Charging Point Quota $q$', fontsize=18)
    plt.ylabel('Execution Time (ms)', fontsize=18)
    plt.title('Execution Time', fontsize=18)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.xticks(xtick_values)
    plt.grid(True)
    plt.savefig(f'execution_time_varyingQ_n_ev{n_ev}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    # Plot 2
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='CP Queue', y='Total charge transferred in-net', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel(r'Charging Point Quota $q$', fontsize=18)
    plt.ylabel('Total Charge Transferred In-net (kWh)', fontsize=18)
    plt.title('In-net Charge Transfer', fontsize=18)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.xticks(xtick_values)
    plt.grid(True)
    plt.savefig(f'In-net_Charge_Transfer_varyingQ_n_ev{n_ev}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    ## Plot 3
    # data2 = data[data['Method'] !='random_elemination']
    data['total SLA missed'] = data['Total SLA breach'] + data['unmatched EV']
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        # if method=='random_elemination':
        #     continue
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='CP Queue', y='total SLA missed', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel(r'Charging Point Quota $q$', fontsize=18)
    plt.ylabel('Missed SLA', fontsize=18)
    plt.title('SLA Analysis', fontsize=18)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.xticks(xtick_values)
    plt.grid(True)
    plt.savefig(f'missed_SLA_varyingQ_n_ev{n_ev}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    ## Plot 4 & 5
    # Filter the data for the required methods
    pcg_data = data[data['Method'] == 'PCG']
    pcd_data = data[data['Method'] == 'PCD']
    
    palette = sns.color_palette("mako", 4)
    
    # Prepare the data for bar plotting
    plot_data = pd.DataFrame({
        'CP Queue': pd.concat([pcg_data['CP Queue'], pcg_data['CP Queue'], pcd_data['CP Queue'], pcd_data['CP Queue']]),
        'EV Charged': pd.concat([pcg_data['Total EV charged in-net'], pcg_data['Total EV charged par-net'], 
                                 pcd_data['Total EV charged in-net'], pcd_data['Total EV charged par-net']]),
        'Category': ['PCG In-net'] * len(pcg_data) + ['PCG par-net'] * len(pcg_data) + 
                    ['PCD In-net'] * len(pcd_data) + ['PCD par-net'] * len(pcd_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='CP Queue', y='EV Charged', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel(r'Charging Point Quota $q$', fontsize=18)
    plt.ylabel('EV Charged', fontsize=18)
    plt.title('EV Assignments', fontsize=18)
    plt.legend(title='Category', fontsize=16, title_fontsize=18, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=16)
    #plt.xticks(xtick_values)
    plt.grid(True)
    plt.savefig(f'EV_Assignments_varyingQ_n_ev{n_ev}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    # plot charge transferred
    palette = sns.color_palette("rocket", 4)
    plot_data = pd.DataFrame({
        'CP Queue': pd.concat([pcg_data['CP Queue'], pcg_data['CP Queue'], pcd_data['CP Queue'], pcd_data['CP Queue']]),
        'EV Charged': pd.concat([pcg_data['Total charge transferred in-net'], pcg_data['Total charge transferred par-net'], 
                                 pcd_data['Total charge transferred in-net'], pcd_data['Total charge transferred par-net']]),
        'Category': ['PCG In-net'] * len(pcg_data) + ['PCG par-net'] * len(pcg_data) + 
                    ['PCD In-net'] * len(pcd_data) + ['PCD par-net'] * len(pcd_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='CP Queue', y='EV Charged', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel(r'Charging Point Quota $q$', fontsize=18)
    plt.ylabel('Total charge transferred (kWh)', fontsize=18)
    plt.title('Transferred Charge', fontsize=18)
    plt.legend(title='Category', fontsize=16, title_fontsize=18, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=16)
    #plt.xticks(xtick_values)
    plt.grid(True)
    plt.savefig(f'Transferred_Charge_varyingQ_n_ev{n_ev}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()

# # Test
# if __name__ == "__main__":
#     csv_file = 'results2.csv'
#     plot_varyingEV(csv_file, 2)

# # Test
# if __name__ == "__main__":
#     csv_file = 'results_varying_Q_2.csv'
#     plot_varyingQ(csv_file, 45)



