#!/usr/bin/env python3
import sys
import json
import itertools
import hashlib

V = 19
K = 3
T = 2
MAX_TICKETS = 58 

def get_flag(tickets):
    normalized = sorted([tuple(sorted(t)) for t in tickets])
    payload = json.dumps(normalized).encode()
    h = hashlib.sha256(payload).hexdigest()[:16]
    return f"CodeVinci{{not_real_flag_{h}}}"

def verify_coverage(user_tickets):
    if len(user_tickets) > MAX_TICKETS:
        return False, f"Too many tickets! ({len(user_tickets)} > {MAX_TICKETS})"
    
    all_pairs_needed = set(itertools.combinations(range(V), T))
    covered_pairs = set()

    for i, ticket in enumerate(user_tickets):
        if len(ticket) != K:
            return False, f"Ticket #{i} invalid: {ticket} (expected {K} numbers)"
        if any(x < 0 or x >= V for x in ticket):
            return False, f"Numbers out of range (0-{V-1})"
        
        pairs = itertools.combinations(ticket, T)
        covered_pairs.update(pairs)

    missing = all_pairs_needed - covered_pairs
    if not missing:
        return True, "OK"
    else:
        return False, f"Incomplete coverage! {len(missing)} pairs missing."

def main():
    print(f"--- LOTTERY ---")
    print(f"V={V}, K={K}, T={T}")
    print(f"Max tickets: {MAX_TICKETS}")
    print("Enter your tickets as a JSON list.")

    try:
        raw_data = sys.stdin.read(1024*1024)
        if not raw_data: return
            
        tickets = json.loads(raw_data)
        if not isinstance(tickets, list):
            print("Invalid JSON: must be a list.")
            return

        success, msg = verify_coverage(tickets)
        
        if success:
            print("Valid solution.")
            print(f"FLAG: {get_flag(tickets)}")
        else:
            print(f"Error: {msg}")

    except json.JSONDecodeError:
        print("Invalid JSON")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
