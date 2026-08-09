ui = false

api_addr = "http://127.0.0.1:8200"

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true
}

storage "inmem" {}

seal "static" {
  current_key_id = "local-compose-key"
  current_key    = "env://OPENBAO_UNSEAL_KEY"
}

initialize "nabi" {
  request "enable-secrets" {
    operation = "update"
    path      = "sys/mounts/secret"
    data = {
      type = "kv"
      options = {
        version = "2"
      }
    }
  }

  request "create-policy" {
    operation = "update"
    path      = "sys/policies/acl/nabi-app"
    data = {
      policy = <<-EOT
        path "secret/data/+" {
          capabilities = ["read"]
        }
      EOT
    }
  }

  request "store-api-key" {
    operation = "update"
    path      = "secret/data/nabi"
    data = {
      data = {
        NABI_API_KEY = {
          eval_type       = "string"
          eval_source     = "env"
          env_var         = "NABI_API_KEY"
          require_present = true
        }
      }
    }
  }

  request "store-flag-api-key" {
    operation = "update"
    path      = "secret/data/flag"
    data = {
      data = {
        FLAG_API_KEY = {
          eval_type       = "string"
          eval_source     = "env"
          env_var         = "FLAG_API_KEY"
          require_present = true
        }
      }
    }
  }

  request "create-app-token" {
    operation = "update"
    path      = "auth/token/create"
    data = {
      id = {
        eval_type       = "string"
        eval_source     = "env"
        env_var         = "OPENBAO_APP_TOKEN"
        require_present = true
      }
      policies         = ["nabi-app"]
      no_parent        = true
      no_default_policy = true
      renewable        = false
    }
  }
}
