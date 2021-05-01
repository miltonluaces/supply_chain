from utilities.std_imports import *
pd.set_option('display.max_columns', None)
from supply_chain.scm.plan import Plan


def brute_force_planning(po, max_npo, min_repl, max_repl, horizon):
    def bfp(po, npo, p, pos):
        pO = np.copy(po)
        if p==horizon or npo==max_npo: 
            #print('Complete ', npo)
            pos.append(pO)
            return
        #print(npo)
        for r in range(min_repl, max_repl+1):
            if(p+r > horizon):
                continue
            pO = np.copy(po)
            pO[p+r] = 1
            bfp(pO, npo+1, p+r, pos)

    pos = []            
    bfp(po=po, npo=1, p=3, pos=pos)
    return pos

# given plan and pos_pos generate pos
def gen_po(plan, pos_idx):
    stock_ini = plan.plan.loc['Stock'][pos_idx[0]-1]
    pos = []
    for i in range(0, len(pos_idx)-1):
         pos.append(plan.plan.loc['Dmd'][pos_idx[i]:pos_idx[i+1]].sum())

    po = np.zeros(plan.horizon+1)
    for i in range(0, len(pos_idx)-1):
        po[pos_idx[i]] = pos[i]
    return po


def get_first_neg(plan):
    for p in range(0, plan.horizon+1):
        if plan.plan.loc['Stock'][p]<=0: 
            return p

        
def pbin2pidx(pb):
    pb[len(pb)-1] = 1
    return np.where(pb==1)[0]


def plan_optimization(plan, pbin):
    best_po = None
    best_cost = np.inf
    for pb in pbin:
        pidx = pbin2pidx(pb)
        po = gen_po(plan, pidx)
        plan.set_po(po)
        cost = plan.get_tot_cost()
        if cost < best_cost:
            best_cost = cost
            best_po = po
    return best_cost, best_po
        
    
    
# npo = random between 1 and 6
# random no rep npo between [firstPo, 20], with firstPo in first negative
# calculate order quantitites (aritmetics)

# another possibility: sequence of periods: 2,3,7 (until 20)

# another posssibility: backtracking 0/1 prune on increasing 



# Minimize total cost while avoiding stockouts

# display hol, tr fix , tr var and total cost per period of a Planning solution (pl orders)
# each time goes to zero if that subplan is optimal it will continue being for overall plan (?) No.
# top down: one order covering all, then split if it improves cost until it doesnt

# Reorder point is pure arithmetics so quantities is the independent variable. Should be equal sum of dmds so, number of periods. Sequence of number of periods 
# until horizon

# Linear programming?