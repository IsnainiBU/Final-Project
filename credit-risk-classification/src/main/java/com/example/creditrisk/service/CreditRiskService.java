package com.example.creditrisk.service;

import com.example.creditrisk.model.CreditRisk;
import com.example.creditrisk.repository.CreditRiskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpMethod;

import java.util.HashMap;
import java.util.Map;

@Service
public class CreditRiskService {
    @Autowired
    private CreditRiskRepository creditRiskRepository;

    private final RestTemplate restTemplate = new RestTemplate();
    private final String flaskApiUrl = "http://127.0.0.1:5000/api/predict"; // Endpoint Flask

    public String[] predictRisk(CreditRisk creditRisk) {
        // Siapkan data untuk dikirim ke Flask API
        Map<String, Object> requestData = new HashMap<>();
        requestData.put("Age", creditRisk.getAge());
        requestData.put("Sex", creditRisk.getSex());
        requestData.put("Job", creditRisk.getJob());
        requestData.put("Housing", creditRisk.getHousing());
        requestData.put("Saving accounts", creditRisk.getSavingAccounts());
        requestData.put("Checking account", creditRisk.getCheckingAccount());
        requestData.put("Credit amount", creditRisk.getCreditAmount());
        requestData.put("Duration", creditRisk.getDuration());
        requestData.put("Purpose", creditRisk.getPurpose());

        try {
            // Header untuk permintaan HTTP
            HttpHeaders headers = new HttpHeaders();
            headers.set("Content-Type", "application/json");

            // Kirim data ke Flask API
            HttpEntity<Map<String, Object>> request = new HttpEntity<>(requestData, headers);
            ResponseEntity<Map> response = restTemplate.exchange(flaskApiUrl, HttpMethod.POST, request, Map.class);

            // Ambil hasil prediksi dari respons
            Map<String, Object> responseBody = response.getBody();
            Double probability =(Double)responseBody.get("probability");
            return responseBody != null ?  new String[]{(String)responseBody.get("risk"), probability.toString()} :  new String[]{"Unknown"};
        } catch (Exception e) {
            e.printStackTrace();
            return  new String[] {"Error: " + e.getMessage()};
        }
        
    }
    public void save(CreditRisk creditRisk) {
        creditRiskRepository.save(creditRisk);
    }
}
