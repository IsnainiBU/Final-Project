package com.example.creditrisk.controller;

import com.example.creditrisk.model.CreditRisk;
import com.example.creditrisk.service.CreditRiskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class CreditRiskController {

    @Autowired
    private CreditRiskService creditRiskService;

    // Endpoint untuk menangani POST request dan mengembalikan prediksi risiko
    @PostMapping("/predict")
    public ResponseEntity<Map<String, String>> predictCreditRisk(@RequestBody CreditRisk creditRisk) {
        // Lakukan prediksi berdasarkan data yang diterima
        String[] risk = creditRiskService.predictRisk(creditRisk);

        // Menyimpan hasil prediksi ke dalam objek CreditRisk
        creditRisk.setRisk(risk[0]);
        creditRisk.setProbability(Double.parseDouble(risk[1]));  // Pastikan konversi ke tipe Double jika perlu

        // Simpan ke database
        creditRiskService.save(creditRisk);

        // Menyiapkan response dengan hasil prediksi risiko
        Map<String, String> response = new HashMap<>();

        response.put("risk", risk[0]);
        response.put("probability", risk[1]);

        // Kembalikan response dengan status OK
        return ResponseEntity.ok(response);

    }
}
