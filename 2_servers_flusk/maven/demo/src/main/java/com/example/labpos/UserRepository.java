package com.example.labpos;

import javax.annotation.PostConstruct;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.Scanner;

import stateless.soap.example.pos.loginuser.Role;
import stateless.soap.example.pos.loginuser.User;
import org.springframework.stereotype.Component;

@Component
public class UserRepository {
    private static final Map<String, User> users = new HashMap<>();

    public void initData() {
        User nelu = new User();
        nelu.setName("nelu");
        nelu.setId(1);
        nelu.setParola("nelu");
        nelu.setRole(Role.ADMIN);


        users.put(nelu.getName(), nelu);

        User emi = new User();
        emi.setName("emi");
        emi.setId(2);
        emi.setParola("emi");
        emi.setRole(Role.AUTOR);

        users.put(emi.getName(), emi);

    }

    public int userExists(String name, String pass) {
        System.out.println(users);
        User u1 = users.get(name);
        if (u1.getParola().equals(pass)) {
            return u1.getId();
        }
        return 0;
    }

    public String createFilePopulate(String name) {
        User u1 = users.get(name);
        Random rnd = new Random();
        String file = "filename" + rnd.nextInt() + ".txt";
        try {
            String dePusInFisier = "" + u1.getId() + "\n" + u1.getName() + "\n" + u1.getRole();
            FileWriter myObj = new FileWriter(file);
            myObj.write(dePusInFisier);
            myObj.close();
        } catch (IOException o) {
            System.out.println("An error occured");
            o.printStackTrace();
        }
        return file;
    }

    public String returnRole(String fileName, int id)
    {
        try{
            File myObj = new File(fileName);
            Scanner myReader = new Scanner(myObj);
            int idd = Integer.parseInt(myReader.nextLine());
            if(id == idd) {
                String name = myReader.nextLine();
                return myReader.nextLine();
            }
        }
        catch (FileNotFoundException e)
        {
            System.out.println("An error occured");
            e.printStackTrace();
        }
        return "404 Not Found";
    }

    public String deleteFile(String file, int id)
    {
        try{
            File myObj = new File(file);
            Scanner myReader = new Scanner(myObj);
            int idd = Integer.parseInt(myReader.nextLine());
            if(id == idd) {
                myObj.delete();
                return "Deleted";
            }
        }
        catch (FileNotFoundException e)
        {
            System.out.println("An error occured");
            e.printStackTrace();
        }
        return "404 Not Found";
    }

}