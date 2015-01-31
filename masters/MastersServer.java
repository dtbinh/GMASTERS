package masters;

import py4j.GatewayServer;

class MastersServer {

    private Masters masters;

    public Masters getMasters() {
        return masters;
    }

    public MastersServer() {
        masters = new Masters();
    }

    public static void main(String[] args) {
        GatewayServer server = new GatewayServer(new MastersServer());
        server.start();
        System.out.println("Masters Server Started");
    }

}
