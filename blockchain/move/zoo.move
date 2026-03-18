// Move — Aptos / Sui
// Deploy on Aptos: aptos move publish
// Deploy on Sui:   sui move build && sui client publish

module intergalactic_zoo::zoo {

    use std::string::{Self, String};
    use std::vector;
    use std::signer;
    use aptos_framework::account;
    use aptos_framework::timestamp;
    use aptos_framework::event::{Self, EventHandle};

    // -----------------------------------------------------------------------
    // Constants
    // -----------------------------------------------------------------------
    const E_NOT_OWNER: u64         = 1;
    const E_REGISTRY_EXISTS: u64   = 2;
    const E_ORGANISM_NOT_FOUND: u64 = 3;
    const E_INVALID_INTELLIGENCE: u64 = 4;

    // -----------------------------------------------------------------------
    // Structs
    // -----------------------------------------------------------------------
    struct Organism has copy, drop, store {
        id:           u64,
        name:         String,
        planet:       String,
        intelligence: u8,
        owner:        address,
        created_at:   u64,
    }

    struct ZooRegistry has key {
        organisms:         vector<Organism>,
        next_id:           u64,
        mint_events:       EventHandle<MintEvent>,
        transfer_events:   EventHandle<TransferEvent>,
    }

    // -----------------------------------------------------------------------
    // Events
    // -----------------------------------------------------------------------
    struct MintEvent has drop, store {
        id:     u64,
        name:   String,
        planet: String,
        owner:  address,
    }

    struct TransferEvent has drop, store {
        id:        u64,
        from:      address,
        to:        address,
    }

    // -----------------------------------------------------------------------
    // Entry functions
    // -----------------------------------------------------------------------

    /// Initialise the zoo for the caller account.
    public entry fun initialize(account: &signer) {
        let addr = signer::address_of(account);
        assert!(!exists<ZooRegistry>(addr), E_REGISTRY_EXISTS);
        move_to(account, ZooRegistry {
            organisms:       vector::empty(),
            next_id:         0,
            mint_events:     account::new_event_handle<MintEvent>(account),
            transfer_events: account::new_event_handle<TransferEvent>(account),
        });
    }

    /// Register a new organism.
    public entry fun register_organism(
        account:      &signer,
        name:         vector<u8>,
        planet:       vector<u8>,
        intelligence: u8,
    ) acquires ZooRegistry {
        assert!(intelligence <= 100, E_INVALID_INTELLIGENCE);
        let addr     = signer::address_of(account);
        let registry = borrow_global_mut<ZooRegistry>(addr);
        let id       = registry.next_id;
        registry.next_id = id + 1;

        let org = Organism {
            id,
            name:         string::utf8(name),
            planet:       string::utf8(planet),
            intelligence,
            owner:        addr,
            created_at:   timestamp::now_seconds(),
        };
        event::emit_event(&mut registry.mint_events, MintEvent {
            id,
            name:   org.name,
            planet: org.planet,
            owner:  addr,
        });
        vector::push_back(&mut registry.organisms, org);
    }

    /// Transfer an organism by ID to a new owner.
    public entry fun transfer_organism(
        account:   &signer,
        registry_owner: address,
        id:        u64,
        new_owner: address,
    ) acquires ZooRegistry {
        let caller   = signer::address_of(account);
        let registry = borrow_global_mut<ZooRegistry>(registry_owner);
        let len      = vector::length(&registry.organisms);
        let i        = 0u64;
        while (i < len) {
            let org = vector::borrow_mut(&mut registry.organisms, i);
            if (org.id == id) {
                assert!(org.owner == caller, E_NOT_OWNER);
                event::emit_event(&mut registry.transfer_events, TransferEvent {
                    id,
                    from: caller,
                    to:   new_owner,
                });
                org.owner = new_owner;
                return
            };
            i = i + 1;
        };
        abort E_ORGANISM_NOT_FOUND
    }

    // -----------------------------------------------------------------------
    // View functions
    // -----------------------------------------------------------------------
    #[view]
    public fun total_organisms(registry_owner: address): u64 acquires ZooRegistry {
        borrow_global<ZooRegistry>(registry_owner).next_id
    }
}
