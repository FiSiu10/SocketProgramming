package ics200.lab5;

import java.io.*;
import java.net.*;

//java ics200.lab5.ServerA 10000

public class ServerA{
    public static void main(String[] args) throws IOException {
        int port = Integer.parseInt(args[0]);
        ServerSocket serverSocket = new ServerSocket(port);
        Socket sock;
        BufferedInputStream bin;
        BufferedOutputStream bout;

        while (true){
            sock = serverSocket.accept();
            bin = new BufferedInputStream(sock.getInputStream());
            bout = new BufferedOutputStream(sock.getOutputStream());

            String ready = "READY";
            bout.write(ready.getBytes("UTF-8"));
            bout.flush();

            byte[] packet = new byte[1024];
            bin.read(packet);

            int operator = packet[0];
            int numberOfOp = packet[1];
            int total = 0; 
            int i = 0;
            
            if (operator == 1){ 
                while (numberOfOp > 0){
                    int a = packet[2+i];
                    //System.out.println("packet a " + a);
                    int number1 = (a & 0xf0) >>> 4;
                    //System.out.println("number1 " + number1);
                    int number2 = a & 0x0f;
                    //System.out.println("number2 " + number2);

                    total = total + number1 + number2;
                    //System.out.println("total " + total);
                    i += 1;
                    numberOfOp -= 2;
                }
                 
            }

            if (operator == 2){
                while (numberOfOp > 0){
                    int a = packet[2+i];
                    //System.out.println("Packet " + a);
                    int b = (a & 0xf0) >>> 4;
                    //System.out.println("value 1: " + b);
                    int c = a & 0x0f;
                    //System.out.println("value 2: " + c);
                    
                    if (i == 0){
                        total = b - c;
                    }
                    else{
                        total = total - b - c;
                    }

                    i += 1;
                    numberOfOp -= 2;
                }
            }
                
            if (operator == 4){
                while (numberOfOp > 0){
                    int a = packet[2+i];
                    //System.out.println("Packet " + a);
                    int b = (a & 0xf0) >>> 4;
                    //System.out.println("value 1: " + b);
                    int c = a & 0x0f;
                    //System.out.println("value 2: " + c);

                    if (i == 0){
                        total = b * c;
                    }
                    else{
                        if (c == 0){
                            total = total * b;
                        }
                        else {
                            total = total * b * c;
                        }
                    }

                    i += 1;
                    numberOfOp -= 2;
                }             
            }
           
            byte[] packet2 = new byte[4];
            packet2[0] = (byte) ((total & 0xff000000) >> 24);
            packet2[1] = (byte) ((total & 0x00ff0000) >> 16);
            packet2[2] = (byte) ((total & 0x0000ff00) >> 8);
            packet2[3] = (byte) ((total & 0x000000ff));

            bout.write(packet2);
            bout.flush();
        }
    }
}
