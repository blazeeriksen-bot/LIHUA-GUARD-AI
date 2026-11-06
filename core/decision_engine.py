class DecisionEngine:

    def analyze(self, threat_score):

        if threat_score >= 80:
            return "LOCKDOWN"

        elif threat_score >= 50:
            return "WARNING"

        else:
            return "SAFE"