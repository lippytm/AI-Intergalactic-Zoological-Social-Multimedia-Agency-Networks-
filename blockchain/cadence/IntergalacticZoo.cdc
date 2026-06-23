// Cadence — Flow Blockchain
// Deploy: flow project deploy

/// IntergalacticZoo: NFT-style organism registry on the Flow blockchain.
pub contract IntergalacticZoo {

    // -----------------------------------------------------------------------
    // Events
    // -----------------------------------------------------------------------
    pub event OrganismMinted(id: UInt64, name: String, planet: String, owner: Address)
    pub event OrganismTransferred(id: UInt64, from: Address, to: Address)
    pub event ContractInitialized()

    // -----------------------------------------------------------------------
    // Storage paths
    // -----------------------------------------------------------------------
    pub let CollectionStoragePath:  StoragePath
    pub let CollectionPublicPath:   PublicPath
    pub let MinterStoragePath:      StoragePath

    // -----------------------------------------------------------------------
    // Total supply
    // -----------------------------------------------------------------------
    pub var totalSupply: UInt64

    // -----------------------------------------------------------------------
    // NFT Resource
    // -----------------------------------------------------------------------
    pub resource Organism {
        pub let id:           UInt64
        pub let name:         String
        pub let planet:       String
        pub let intelligence: UInt8
        pub let mintedAt:     UFix64

        init(id: UInt64, name: String, planet: String, intelligence: UInt8) {
            pre { intelligence <= 100 : "Intelligence must be 0–100" }
            self.id           = id
            self.name         = name
            self.planet       = planet
            self.intelligence = intelligence
            self.mintedAt     = getCurrentBlock().timestamp
        }
    }

    // -----------------------------------------------------------------------
    // Collection
    // -----------------------------------------------------------------------
    pub resource interface CollectionPublic {
        pub fun borrowOrganism(id: UInt64): &Organism?
        pub fun getIDs(): [UInt64]
        pub fun count(): Int
    }

    pub resource Collection: CollectionPublic {
        pub var organisms: @{UInt64: Organism}

        init() { self.organisms <- {} }

        pub fun deposit(organism: @Organism) {
            let id = organism.id
            let old <- self.organisms[id] <- organism
            destroy old
        }

        pub fun withdraw(id: UInt64): @Organism {
            let organism <- self.organisms.remove(key: id)
                ?? panic("Organism not found: ".concat(id.toString()))
            return <- organism
        }

        pub fun borrowOrganism(id: UInt64): &Organism? {
            return &self.organisms[id] as &Organism?
        }

        pub fun getIDs(): [UInt64] { return self.organisms.keys }

        pub fun count(): Int { return self.organisms.length }

        destroy() { destroy self.organisms }
    }

    pub fun createEmptyCollection(): @Collection {
        return <- create Collection()
    }

    // -----------------------------------------------------------------------
    // Minter
    // -----------------------------------------------------------------------
    pub resource Minter {
        pub fun mint(
            name:         String,
            planet:       String,
            intelligence: UInt8,
        ): @Organism {
            IntergalacticZoo.totalSupply = IntergalacticZoo.totalSupply + 1
            let org <- create Organism(
                id:           IntergalacticZoo.totalSupply,
                name:         name,
                planet:       planet,
                intelligence: intelligence,
            )
            return <- org
        }
    }

    // -----------------------------------------------------------------------
    // Initialiser
    // -----------------------------------------------------------------------
    init() {
        self.totalSupply             = 0
        self.CollectionStoragePath   = /storage/IntergalacticZooCollection
        self.CollectionPublicPath    = /public/IntergalacticZooCollection
        self.MinterStoragePath       = /storage/IntergalacticZooMinter

        self.account.save(<- create Minter(), to: self.MinterStoragePath)
        self.account.save(<- create Collection(), to: self.CollectionStoragePath)
        self.account.link<&Collection{CollectionPublic}>(
            self.CollectionPublicPath,
            target: self.CollectionStoragePath
        )
        emit ContractInitialized()
    }
}
