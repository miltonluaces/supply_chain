from utilities.std_imports import *
pd.set_option('display.max_columns', None)

# Basic methods

def create_plan(pl_hor, dmd, fo, on_hand):
    pers = list(range(pl_hor+1))
    plan = pd.DataFrame(columns=pers)
    plan.loc[0] = dmd
    plan.loc[1] = fo
    plan.loc[2] = np.zeros(pl_hor+1)
    plan.loc[3] = np.zeros(pl_hor+1)
    plan.loc[4] = np.zeros(pl_hor+1)
    plan.loc[5] = np.zeros(pl_hor+1)
    plan.index = ['Demand', 'FiOrders', 'PlOrders_Rcp', 'PlOrders_Rel', 'Proj_Stk', 'Proj_Stk_PO']
    plan.loc['Proj_Stk'][0] = on_hand
    plan.loc['Proj_Stk_PO'][0] = on_hand
    return plan 

def upd_stk(plan):
    pl_hor = plan.shape[1]-1
    for i in range(1, pl_hor+1):
        plan.loc['Proj_Stk'][i] = plan.loc['Proj_Stk_PO'][i-1] - plan.loc['Demand'][i] + plan.loc['FiOrders'][i]
        plan.loc['Proj_Stk_PO'][i] = plan.loc['Proj_Stk'][i] + plan.loc['PlOrders_Rcp'][i]
    return plan

# Planning strategies

def L4T(plan):
    pl_hor = plan.shape[1]-1
    for i in range(1, pl_hor+1):
        if plan.loc['Demand'][i] > 0: plan.loc['PlOrders_Rcp'][i] = plan.loc['Demand'][i]
        upd_stk(plan)
        
def FOQ(plan, lot_size):
    pl_hor = plan.shape[1]-1
    for i in range(1, pl_hor+1):
        upd_stk(plan)
        if plan.loc['Proj_Stk'][i] <= 0: plan.loc['PlOrders_Rcp'][i] = np.ceil(-plan.loc['Proj_Stk'][i]/lot_size) * lot_size
        upd_stk(plan)

def FOQi(plan, lot_size, increment):
    pl_hor = plan.shape[1]-1
    for i in range(1, pl_hor+1):
        upd_stk(plan)
        if plan.loc['Proj_Stk'][i] <= 0: 
            plan.loc['PlOrders_Rcp'][i] = np.ceil(-plan.loc['Proj_Stk'][i]/increment) * increment
            if plan.loc['PlOrders_Rcp'][i] < lot_size: plan.loc['PlOrders_Rcp'][i] = lot_size
        upd_stk(plan)

def SL(plan):
    pl_hor = plan.shape[1]-1
    upd_stk(plan)
    if plan.loc['Proj_Stk'][pl_hor] <= 0:
        plan.loc['PlOrders_Rcp'][1] = -plan.loc['Proj_Stk'][pl_hor]
    upd_stk(plan)


