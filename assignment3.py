import random

class Node:

    name =""
    parentNames = []
    cpt = []

    def __init__(self, nodeInfo):
        """
        :param nodeInfo: in the format as [name, parents, cpt]
        """
        # name, parents, cpt

        self.name = nodeInfo[0]
        self.parentNames = nodeInfo[1].copy()
        self.cpt = nodeInfo[2].copy()


    def format_cpt(self):
        s_cpt = '\t'.join(self.parentNames) + '\n'
        for i in range(len(self.cpt)):
            s_cpt += bin(i).replace("0b", "").zfill(len(self.parentNames)).replace('0', 'T\t').replace('1', 'F\t')
            s_cpt += str(self.cpt[i]) + '\n'
        return s_cpt


    def print(self):
        print("name: {}\nparents:{}\ncpt:\n{}".format(self.name, self.parentNames, self.format_cpt()))


class BayesNet:
    nodes = []

    def __init__(self, nodeList):
        for n in nodeList:
            self.nodes.append(Node(n))

    def print(self):
        for n in self.nodes:
            n.print()

    def rejectionSampling(self, qVar, evidence, N):
        """
        :param qVar: query variable
        :param evidence: evidence variables and their values in a dictionary
        :param N: maximum number of iterations
        E.g. ['WetGrass',{'Sprinkler':True, 'Rain':False}, 10000]
        :return: probability distribution for the query
        """
        C = [0, 0]

        for i in range(0, N):
            x = self.prior_sample()

            if self.is_consistent(x, evidence):
                query = x[qVar]
                j = 0 if query else 1
                C[j] += 1

        return self.normalize(C)
    
    def normalize(self, C):
        normalized_C = []
        total = sum(C)

        if total == 0:
            return C

        for i in range(len(C)):
            normalized_C.append(C[i] / total)

        return normalized_C
    
    def is_consistent(self, x, evidence):
        for var in evidence:
            if x[var] != evidence[var]:
                return False
        
        return True
    
    def prior_sample(self):
        x = {}
        n = len(self.nodes)

        for i in range(n):
            node = self.nodes[i]
            parents = node.parentNames

            if len(parents) == 0:
                x[node.name] = self.generate_event(node.cpt[0])
            else:
                idx = self.find_index(x, node.parentNames)
                x[node.name] = self.generate_event(node.cpt[idx])
        
        return x
    
    def find_index(self, x, parentNames):
        lo = 0
        hi = 2 ** len(parentNames) - 1

        for parent in parentNames:
            result = x[parent]

            if result:
                diff = (hi - lo) + 1
                diff = diff // 2
                hi -= diff
            else:
                diff = (hi - lo) + 1
                diff = diff // 2
                lo += diff
        
        return lo
                
    def generate_event(self, probability):
        return random.random() < probability

    def gibbsSampling(self, qVar, evidence, N):
        """
                :param qVar: query variable
                :param evidence: evidence variables and their values in a dictionary
                :param N: maximum number of iterations
                E.g. ['WetGrass',{'Sprinkler':True, 'Rain':False}, 10000]
                :return: probability distribution for the query
                """
        C = [0, 0]
        Z = self.get_non_evidence(evidence)
        x = self.initialize_dict(evidence, Z)
        Z_i = self.choose_variable(Z)

        for k in range(N):
            Z_i = self.choose_variable(Z)
            P = self.sample_markov_blanket(x, Z_i)
            x[Z_i.name] = self.generate_event(P[0])
            query = x[qVar]
            j = 0 if query else 1
            C[j] += 1
        
        return self.normalize(C)
    
    def choose_variable(self, Z):
        return random.choice(Z)
    
    def sample_markov_blanket(self, x, Z_i):
        P = [0, 0]
        children = self.get_children(Z_i)
        tmp = x[Z_i.name]

        for j in range(2):
            if j == 0:
                x[Z_i.name] = True
            else:
                x[Z_i.name] = False
            
            probability = self.get_conditional_probability(x, Z_i)
            
            for i in range(len(children)):
                child = children[i]
                p2 = self.get_conditional_probability(x, child)
                probability *= p2
            
            x[Z_i.name] = tmp
            P[j] = probability

        return self.normalize(P)
        
    def get_conditional_probability(self, x, Z_i):
        parents = Z_i.parentNames
        probability = 1

        if len(parents) == 0:
            probability *= Z_i.cpt[0]
        else:
            idx = self.find_index(x, parents)
            probability *= Z_i.cpt[idx]
        
        if not x[Z_i.name]:
            probability = 1 - probability
        
        return probability
    
    def get_children(self, node):
        children = []
        n = len(nodes)

        for i in range(n):
            current = self.nodes[i]

            if node.name in current.parentNames:
                children.append(current)
        
        return children
    
    def initialize_dict(self, evidence, Z):
        x = {}

        for var in evidence:
            x[var] = evidence[var]
        
        for i in range(len(Z)):
            node = Z[i]
            x[node.name] = self.generate_event(0.5)
        
        return x
    
    def get_non_evidence(self, evidence):
        non_evidence = []
        n = len(self.nodes)

        for i in range(n):
            node = self.nodes[i]

            if node.name not in evidence:
                non_evidence.append(node)

        return non_evidence

# Sample Bayes net
nodes = [["Cloudy", [], [0.5]],
 ["Sprinkler", ["Cloudy"], [0.1, 0.5]],
 ["Rain", ["Cloudy"], [0.8, 0.2]],
 ["WetGrass", ["Sprinkler", "Rain"], [0.99, 0.9, 0.9, 0.0]]]
b = BayesNet(nodes)
b.print()


print(b.rejectionSampling("Rain", {"Sprinkler":True}, 100000))

# Sample queries to test your code
print(b.gibbsSampling("Rain", {"Sprinkler":True}, 100000))
