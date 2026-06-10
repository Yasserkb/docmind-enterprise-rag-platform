package com.docmind.gateway.config;

import java.security.Principal;
import org.springframework.cloud.gateway.filter.ratelimit.KeyResolver;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import reactor.core.publisher.Mono;

@Configuration
class RateLimitConfig {
    @Bean
    KeyResolver principalOrIpKeyResolver() {
        return exchange -> exchange.getPrincipal()
                .map(Principal::getName)
                .switchIfEmpty(Mono.just(exchange.getRequest().getRemoteAddress() == null
                        ? "anonymous"
                        : exchange.getRequest().getRemoteAddress().getAddress().getHostAddress()));
    }
}
