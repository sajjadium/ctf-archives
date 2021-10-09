From CTF Require Simpl.
From CTF Require SimplChall.

Check SimplChall.confidence_hides_imp_expr:
  forall e l, Simpl.confident_expr e l -> Simpl.usesConfidentExpr e l = false.

Check SimplChall.confidence_hides_imp_stmt:
  forall s, Simpl.P_confidence_hides_imp_stmt s.

