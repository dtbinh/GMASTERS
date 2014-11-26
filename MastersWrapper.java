import org.nlogo.headless.HeadlessWorkspace;

public class MastersWrapper {
  public static void main(String[] argv) {
    HeadlessWorkspace workspace = HeadlessWorkspace.newInstance() ;
    try {
      workspace.open("Masters_vBETA.nlogo3d");
      // Set random seed for reproducible experiments
      workspace.command("random-seed 0");
      // Clear all
      workspace.command("ca");
      // Set simulation parameters
      workspace.command("set parameters \"5-0.5-0.5-1-1-1-500\"");
      // Runs the simulation
      workspace.command("run_masters");

      // Print reporters
      System.out.println(workspace.report("ask_energy"));
      System.out.println(workspace.report("ask_energy_tick"));
      System.out.println(workspace.report("ask_best_energia"));
      workspace.dispose();
    }
    catch(Exception ex) {
      ex.printStackTrace();
    }
  }
}
