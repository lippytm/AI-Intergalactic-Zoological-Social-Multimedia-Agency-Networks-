;; Clarity — Stacks Blockchain
;; Deploy: clarinet deploy  |  Test: clarinet test

;; ---------------------------------------------------------------------------
;; Traits
;; ---------------------------------------------------------------------------
(define-trait organism-registry-trait
  (
    (mint-organism (principal (string-ascii 64) (string-ascii 64) uint) (response uint uint))
    (transfer-organism (uint principal) (response bool uint))
    (get-organism (uint) (optional { name: (string-ascii 64), planet: (string-ascii 64),
                                      intelligence: uint, owner: principal }))
  )
)

;; ---------------------------------------------------------------------------
;; Constants
;; ---------------------------------------------------------------------------
(define-constant CONTRACT-OWNER tx-sender)
(define-constant ERR-NOT-AUTHORISED  (err u100))
(define-constant ERR-TOKEN-NOT-FOUND (err u101))
(define-constant ERR-NOT-OWNER       (err u102))
(define-constant ERR-INVALID-IQ      (err u103))

;; ---------------------------------------------------------------------------
;; Data variables
;; ---------------------------------------------------------------------------
(define-data-var next-token-id uint u0)

;; ---------------------------------------------------------------------------
;; Data maps
;; ---------------------------------------------------------------------------
(define-map organisms
  { token-id: uint }
  { name: (string-ascii 64), planet: (string-ascii 64),
    intelligence: uint, owner: principal, minted-at: uint }
)

(define-map minter-whitelist principal bool)

;; ---------------------------------------------------------------------------
;; Events (via print)
;; ---------------------------------------------------------------------------
(define-private (emit-mint-event (token-id uint) (owner principal) (name (string-ascii 64)))
  (print { event: "organism-minted", token-id: token-id, owner: owner, name: name })
)

;; ---------------------------------------------------------------------------
;; Public functions
;; ---------------------------------------------------------------------------

;; Authorise a minter
(define-public (set-minter (minter principal) (authorised bool))
  (begin
    (asserts! (is-eq tx-sender CONTRACT-OWNER) ERR-NOT-AUTHORISED)
    (map-set minter-whitelist minter authorised)
    (ok true)
  )
)

;; Mint an organism
(define-public (mint-organism
    (to           principal)
    (name         (string-ascii 64))
    (planet       (string-ascii 64))
    (intelligence uint))
  (let ((token-id (+ (var-get next-token-id) u1)))
    (asserts! (or (is-eq tx-sender CONTRACT-OWNER)
                  (default-to false (map-get? minter-whitelist tx-sender)))
              ERR-NOT-AUTHORISED)
    (asserts! (<= intelligence u100) ERR-INVALID-IQ)
    (var-set next-token-id token-id)
    (map-set organisms { token-id: token-id }
      { name: name, planet: planet, intelligence: intelligence,
        owner: to, minted-at: block-height })
    (emit-mint-event token-id to name)
    (ok token-id)
  )
)

;; Transfer an organism
(define-public (transfer-organism (token-id uint) (new-owner principal))
  (let ((org (unwrap! (map-get? organisms { token-id: token-id }) ERR-TOKEN-NOT-FOUND)))
    (asserts! (is-eq (get owner org) tx-sender) ERR-NOT-OWNER)
    (map-set organisms { token-id: token-id }
      (merge org { owner: new-owner }))
    (print { event: "organism-transferred", token-id: token-id,
             from: tx-sender, to: new-owner })
    (ok true)
  )
)

;; ---------------------------------------------------------------------------
;; Read-only functions
;; ---------------------------------------------------------------------------

(define-read-only (get-organism (token-id uint))
  (map-get? organisms { token-id: token-id })
)

(define-read-only (total-supply)
  (var-get next-token-id)
)

(define-read-only (is-minter (addr principal))
  (default-to false (map-get? minter-whitelist addr))
)
