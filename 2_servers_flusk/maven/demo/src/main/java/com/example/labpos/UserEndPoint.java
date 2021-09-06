package com.example.labpos;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import stateless.soap.example.pos.loginuser.*;


@Endpoint
public class UserEndPoint {
    private static final String NAMESPACE_URI = "http://pos.example.soap.stateless/LoginUser";

    private UserRepository userRepository;

    @Autowired
    public UserEndPoint(UserRepository userRepository) {
        this.userRepository = userRepository;
        this.userRepository.initData();
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getLoginRequest")
    @ResponsePayload
    public GetLoginResponse getLogin(@RequestPayload GetLoginRequest request) {
        GetLoginResponse response = new GetLoginResponse();
        int id = userRepository.userExists(request.getUser(), request.getParola());
        if (id != 0) {
            response.setId(id);
            response.setName(request.getUser());
            response.setMesaj("200 OK" + "\n" + userRepository.createFilePopulate(request.getUser()));
            System.out.println("macar ajunge aici");

        } else {
            response.setMesaj("404 Not Found");
        }
        System.out.println(response.getMesaj());
        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getRoleRequest")
    @ResponsePayload
    public GetRoleResponse getLogin(@RequestPayload GetRoleRequest request) {
        GetRoleResponse response = new GetRoleResponse();
        response.setRole(userRepository.returnRole(request.getNumeFisier(), request.getId()));
        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "deleteLoginRequest")
    @ResponsePayload
    public DeleteLoginResponse getLogin(@RequestPayload DeleteLoginRequest request) {
        DeleteLoginResponse response = new DeleteLoginResponse();
        response.setMesaj(userRepository.deleteFile(request.getNumeFisier(), request.getId()));
        return response;
    }


}