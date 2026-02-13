from utilities.std_imports import *
pd.set_option('display.max_columns', None)

class Plan:
    
    def __init__(self, horizon, dmd, on_hand):
        self.horizon = horizon
        self.plan = pd.DataFrame(columns=list(range(horizon+1)))
        self.plan.loc[0] = dmd
        self.plan.loc[1] = np.zeros(horizon+1)
        stk = np.zeros(horizon+1)
        stk[0] = on_hand
        self.plan.loc[2] = stk
        self.plan.index = ['Dmd', 'Pl.Or', 'Stock']
        
        self.hol_uc = 0
        self.tr_fix_uc = 0
        self.tr_var_uc = 0
        
    def set_costs(self, hol_uc, tr_fix_uc, tr_var_uc):
        self.hol_uc = hol_uc
        self.tr_fix_uc = tr_fix_uc
        self.tr_var_uc = tr_var_uc
        
    def show(self):
        display(self.plan)       
        
    def upd_stk(self):
        for i in range(1, self.horizon+1):
            self.plan.loc['Stock'][i] = self.plan.loc['Stock'][i-1] - self.plan.loc['Dmd'][i] + self.plan.loc['Pl.Or'][i]
    
    def get_tot_dmd(self):
        return self.plan.loc['Dmd'].sum()
    
    def get_avg_stk(self):
        return round(self.plan.loc['Stock'].mean(),2)
    
    def get_npo(self):
        return len(self.plan.loc['Pl.Or'][self.plan.loc['Pl.Or']>0])
 
    def get_hol_cost(self, end=-1):
        if end == 0: return 0
        if end ==-1: end = self.horizon
        stk_pos = self.plan.loc['Stock'][:end+1][self.plan.loc['Stock'][:end+1]>0].sum()
        hol_cost = round(stk_pos * self.hol_uc,2)
        return round(hol_cost/end,2)
    
    def get_tr_cost(self, end=-1):
        if end == 0: return 0
        if end==-1: end = self.horizon
        po = self.plan.loc['Pl.Or'][:end+1][self.plan.loc['Pl.Or'][:end+1]>0]
        n_po = len(po)
        tot_po = po.sum()
        tr_fix = n_po * self.tr_fix_uc
        tr_var = tot_po * self.tr_var_uc
        tr = tr_fix + tr_var
        return round(tr/end,2)
    
    def get_tot_cost(self, end=-1):
        return round(self.get_hol_cost(end) + self.get_tr_cost(end),2) 
    
    def set_po(self, po):
        self.plan.loc['Pl.Or'] = po
        self.upd_stk()
        
    def show_metrics(self):
        tot_dmd = self.get_tot_dmd()
        avg_stk = self.get_avg_stk()
        n_po = self.get_npo()
        hol_cost = self.get_hol_cost()
        tr_cost = self.get_tr_cost()
        tot_cost = self.get_tot_cost()

        metric_names = ['Total demand', 'Average stock', 'N Pl.orders', 'Holding cost', 'Transport cost', 'Total cost']
        metric_values = [tot_dmd, avg_stk, n_po, hol_cost, tr_cost, tot_cost]
        met = pd.DataFrame({'Metric': metric_names, 'Value': metric_values})
        display(met)
        
    def get_hol_cost_ac(self):
        return  [self.get_hol_cost(end) for end in range(self.horizon+1)]
    
    def get_tr_cost_ac(self):
        return  [self.get_tr_cost(end) for end in range(self.horizon+1)]
    
    def get_tot_cost_ac(self):
        return  [self.get_tot_cost(end) for end in range(self.horizon+1)]
    
    def show_ac_costs(self):
        plan_costs = self.plan
        plan_costs.loc[3] = self.get_hol_cost_ac()
        plan_costs.loc[4] = self.get_tr_cost_ac()
        plan_costs.loc[5] = self.get_tot_cost_ac()
        plan_costs.index = ['Dmd', 'Pl.Or', 'Stock', 'Ho_cost', 'Tr_cost', 'Tot_cost']
        display(plan_costs)