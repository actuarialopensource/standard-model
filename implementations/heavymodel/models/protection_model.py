from heavymodel import Model

class TermAssurance(Model):
    def net_cf(self, t):
        return self.premiums(t) - self.claims(t) - self.expenses(t)
    
    def premium_pp(self, t):
        """monthly premium"""
        return self.annual_premium / 12
    
    def claim_pp(self, t):
        if t == 0:
            return self.sum_assured
        elif t > self.term_y * 12:
            return 0
        elif self.shape == "level":
            return self.sum_assured
        elif self.shape == "decreasing":
            r = (1+0.07)**(1/12)-1
            S = self.sum_assured
            T = self.term_y * 12
            outstanding = S * ((1+r)**T - (1+r)**t)/((1+r)**T - 1)
            return outstanding
        else:
            raise ValueError("Parameter 'shape' must be 'level' or 'decreasing'")
    
    def inflation_factor(self, t):
        """annual"""
        return (1 + self.cost_inflation_pa)**(t//12)
      
    def premiums(self, t):
        return self.premium_pp(t) * self.num_pols_if(t)
    
    def duration(self, t):
        """duration in force in years"""
        return t//12
    
    def claims(self, t):
        return self.claim_pp(t) * self.num_deaths(t)
      
    def expenses(self, t):
       return self.num_pols_if(t) * self.expense_pp/12 * self.inflation_factor(t)
      
    def num_pols_if(self, t):
        """number of policies in force"""
        if t==0:
            return self.init_pols_if
        elif t > self.term_y * 12:
            return 0
        else:
            return self.num_pols_if(t-1) - self.num_exits(t-1) - self.num_deaths(t-1)
    
      
    def num_exits(self, t):
        """exits occurring at time t"""
        return self.num_pols_if(t) * (1-(1 - self.lapse_rate_pa)**(1/12))
      
      
    def num_deaths(self, t):
        """deaths occurring at time t"""
        return self.num_pols_if(t) * self.q_x_12(t)
    
    def age(self, t):
        return self.age_at_entry + t//12
    
    
    def q_x_12(self, t):
        return 1-(1- self.q_x_rated(t))**(1/12)
    
    def qx_non_smoker(self, t):
        """non-smoker mortality"""
        return self.mort_qx_non_smoker[self.age(t), self.duration(t)]
  
    def qx_smoker(self, t):
        """smoker mortality"""
        return self.mort_qx_smoker[self.age(t), self.duration(t)]
    
    def q_x(self, t):
        if self.smoker_status == "N":
            return self.qx_non_smoker(t)
        elif self.smoker_status == "S":
            return self.qx_smoker(t)
            
    def q_x_rated(self, t):
        return max(0, min(1 , self.q_x(t) * (1 + self.extra_mortality) ) )
        
    def commission(self, t):
        return 0
