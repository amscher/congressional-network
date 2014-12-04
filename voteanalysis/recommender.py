import legislators, votes
import numpy as np

def create_vote_matrix(legislators_list, votes_list):
	lid_map = legislators.build_id_map(legislators_list)
	vote_matrix = np.nan * np.ones((len(legislators_list),len(votes_list)))
	for v_i in xrange(len(votes_list)):
		vote_map = votes_list[v_i].get_legislator_vote_map(lid_map)
		for l_i in xrange(len(legislators_list)):
			legislator = legislators_list[l_i]
			if legislator not in vote_map:
				continue
			legislator_vote = vote_map[legislator]
			if legislator_vote == votes.VoteResponse.Aye:
				vote_matrix[l_i][v_i] = 1
			elif legislator_vote == votes.VoteResponse.No:
				vote_matrix[l_i][v_i] = -1
	return np.matrix(vote_matrix)

def get_legislator_bias(r):
	bill_avg = np.nanmean(r,0,keepdims=True)
	legislator_difference = r - bill_avg
	legislator_bias = np.nanmean(legislator_difference,1,keepdims=True)
	legislator_bias = np.nan_to_num(legislator_bias)
	return legislator_bias

def sum_square_error(r, r_hat):
	error = np.nansum(get_squared_error(r,r_hat))
	return error

def get_squared_error(r, r_hat):
	errors = r - r_hat
	squared_error = np.multiply(errors, errors)
	return squared_error

def get_gradient(p,q,r,legislator_bias,beta=0.02):
	r_hat = p * q.T + legislator_bias
	e = r - r_hat
	p_delta = -2 * np.nan_to_num(e) * np.nan_to_num(q) + beta * p #check this
	q_delta = -2 * np.nan_to_num(e.T) * np.nan_to_num(p) + beta * q #np.multiply(-2 * e, p) #check this
	return (p_delta, q_delta)

def update_step(alpha,p,q,r,legislator_bias):
	(p_delta, q_delta) = get_gradient(p,q,r,legislator_bias)
	p_prime = p - alpha * p_delta
	q_prime = q - alpha * q_delta
	return (p_prime, q_prime)

def run_factorization(r, k, steps, alpha, threshold = 0.001):
	n = r.shape[0]
	m = r.shape[1]
	p = np.matrix(np.random.rand(n, k))
	q = np.matrix(np.random.rand(m, k))
	legislator_bias = get_legislator_bias(r)
	errors = list()
	for i in xrange(steps):
		(p,q) = update_step(alpha, p, q, r, legislator_bias)
		errors.append(sum_square_error(r, p*q.T)/float(r.size))
		if (len(errors) > 2 and abs(errors[-1] - errors[-2])/errors[-2] < threshold):
			break
	return (p,q,legislator_bias,errors)

def get_predictions(r_hat):
	threshold = np.vectorize(lambda x: 1 if x >= 0 else -1)
	predictions = threshold(r_hat)
	return predictions