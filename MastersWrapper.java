import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Properties;
import java.io.IOException;
import java.util.Enumeration;

import org.nlogo.headless.HeadlessWorkspace;


public class MastersWrapper {
    public static void main(String[] argv) {
        if (argv.length < 1) {
            System.out.println("usage: ./run_masters_headless <parameters_file>");
        } else {
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

                setSimulationParameters(workspace, argv[0]);
                workspace.command("run_masters");

                System.out.println("\n=== Reporters ===");
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


    public static void setSimulationParameters(HeadlessWorkspace workspace, String filepath) 
            throws Exception {
        Properties prop = loadSimulationParameters(filepath);
        Enumeration<?> e = prop.propertyNames();
        while (e.hasMoreElements()) {
            String key = (String) e.nextElement();
            String value = prop.getProperty(key);
            workspace.command("set " + key + " " + value);
        }
    }


    public static Properties loadSimulationParameters(String filepath) {
        Properties prop = new Properties();
        InputStream input = null;
        try {
            input = new FileInputStream(filepath);
            prop.load(input);
        } catch (IOException ex) {
            ex.printStackTrace();
        } finally {
            if (input != null) {
                try {
                    input.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return prop;
    }

}
