package com.example.creditrisk;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@EntityScan(basePackages = "com.example.creditrisk.model") // Menambahkan ini untuk memastikan Spring memindai paket yang tepat
@EnableJpaRepositories(basePackages = "com.example.creditrisk.repository") // Memastikan repository Anda dipindai
public class CreditRiskClassificationApplication {

	public static void main(String[] args) {
		SpringApplication.run(CreditRiskClassificationApplication.class, args);
	}
}
