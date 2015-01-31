package masters;

import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Properties;
import java.io.IOException;
import java.util.Enumeration;

import org.nlogo.headless.HeadlessWorkspace;


public class Masters {
    
    HeadlessWorkspace workspace;

    public Masters() {
        workspace = HeadlessWorkspace.newInstance();
        try {
            workspace.open("Masters_vBETA.nlogo3d");
            workspace.command("random-seed 0");
        } catch(Exception ex) {
            ex.printStackTrace();
        }
    }

    public void loadParameters(String filename) throws Exception{
        workspace.command("ca");
        System.out.println("Reading parameters from " + filename);
        System.out.println("===========================");
        setSimulationParameters(filename);
        System.out.println("===========================");
        workspace.command("run_masters");
    }

    public void step() throws Exception {
        workspace.command("step");
    }

    public Object is_running() throws Exception {
        return workspace.report("is_running");
    }

    public void printReporters() throws Exception {
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
        System.out.println("\n=== Reporters ===");
        for (String reporter : reporters) {
            System.out.println(reporter + ": " + workspace.report(reporter));
        }
    }

    public void setSimulationParameters(String filepath) 
            throws Exception {
        Properties prop = loadSimulationParameters(filepath);
        Enumeration<?> e = prop.propertyNames();
        while (e.hasMoreElements()) {
            String key = (String) e.nextElement();
            String value = prop.getProperty(key);
            System.out.println(key + " = " + value);
            workspace.command("set " + key + " " + value);
        }
    }

    public Properties loadSimulationParameters(String filepath) {
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
