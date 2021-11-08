import soot.jimple.*;
import soot.jimple.StmtSwitch;
import soot.Value;

public class IrrelevantStmtSwitch implements StmtSwitch
{
    public boolean relevant = true;

    public void caseAssignStmt(AssignStmt stmt)
    {
        boolean phantom = false;

        do {
            if (!soot.options.Options.v().allow_phantom_refs())
                break;

            Value right = stmt.getRightOp();

            if (!(right instanceof InvokeExpr))
                break;

            if (!((InvokeExpr) right).getMethodRef().declaringClass().isPhantom())
                break;

            phantom = true;

        } while (false);

        relevant = !phantom;
    }

    public void caseBreakpointStmt(BreakpointStmt stmt)
    {
        relevant = false;
    }
  
    public void caseEnterMonitorStmt(EnterMonitorStmt stmt)
    {
        relevant = false;
    }
  
    public void caseExitMonitorStmt(ExitMonitorStmt stmt)
    {
        relevant = false;
    }
  
    public void caseGotoStmt(GotoStmt stmt)
    {
        relevant = false;
    }
  
    public void caseIdentityStmt(IdentityStmt stmt)
    {
        relevant = true;
    }

    public void caseIfStmt(IfStmt stmt)
    {
        relevant = false;
    }
  
    public void caseInvokeStmt(InvokeStmt stmt)
    {
        if (soot.options.Options.v().allow_phantom_refs())
            relevant = !stmt.getInvokeExpr().getMethodRef().declaringClass().isPhantom();
        else
            relevant = true;
    }

    public void caseLookupSwitchStmt(LookupSwitchStmt stmt)
    {
        relevant = false;
    }
  
    public void caseNopStmt(NopStmt stmt)
    {
        relevant = true;
    }

    public void caseRetStmt(RetStmt stmt)
    {
        relevant = false;
    }
  
    public void caseReturnStmt(ReturnStmt stmt)
    {
        relevant = true;
    }
  
    public void caseReturnVoidStmt(ReturnVoidStmt stmt)
    {
        relevant = false;
    }
  
    public void caseTableSwitchStmt(TableSwitchStmt stmt)
    {
        relevant = false;
    }
  
    public void caseThrowStmt(ThrowStmt stmt)
    {
        relevant = true; 
    }
  
    public void defaultCase(Object obj)
    {
        throw new RuntimeException("uh, why is this invoked?");
    }
}
