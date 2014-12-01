import org.nlogo.headless.HeadlessWorkspace;

public class MastersWrapper {
  public static void main(String[] argv) {
    HeadlessWorkspace workspace = HeadlessWorkspace.newInstance() ;
    String[] reporters = {
        "ask_energy",
        "ask_energy_tick",
        "ask_best_energia",
        "elapsed",
        "array_x",
        "array_y",
        "array_z",
        "potentials"
    };
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

      for (String reporter : reporters) {
          System.out.println(reporter + ": " + workspace.report(reporter));
      }

      workspace.dispose();
    }
    catch(Exception ex) {
      ex.printStackTrace();
    }
  }
}
