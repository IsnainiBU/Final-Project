package com.example.creditrisk.repository;

import com.example.creditrisk.model.CreditRisk;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CreditRiskRepository extends JpaRepository<CreditRisk, Long> {
}
