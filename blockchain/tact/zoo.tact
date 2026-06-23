// Tact — TON Blockchain smart contract
// Compile: npx blueprint build  |  Deploy via Blueprint

import "@stdlib/deploy";

// ---------------------------------------------------------------------------
// Messages
// ---------------------------------------------------------------------------
message MintOrganism {
    to:           Address;
    name:         String;
    planet:       String;
    intelligence: Int as uint8;
}

message TransferOrganism {
    tokenId:  Int as uint64;
    newOwner: Address;
}

// ---------------------------------------------------------------------------
// Structs
// ---------------------------------------------------------------------------
struct Organism {
    name:         String;
    planet:       String;
    intelligence: Int;
    owner:        Address;
    mintedAt:     Int;
}

// ---------------------------------------------------------------------------
// Contract
// ---------------------------------------------------------------------------
contract IntergalacticZoo with Deployable {

    owner:       Address;
    nextTokenId: Int as uint64;
    organisms:   map<Int, Organism>;

    init(owner: Address) {
        self.owner       = owner;
        self.nextTokenId = 0;
    }

    // -----------------------------------------------------------------------
    // Receivers
    // -----------------------------------------------------------------------
    receive(msg: MintOrganism) {
        require(sender() == self.owner, "Not authorised");
        require(msg.intelligence >= 0 && msg.intelligence <= 100, "Intelligence must be 0-100");

        self.nextTokenId = self.nextTokenId + 1;
        let id: Int = self.nextTokenId;

        self.organisms.set(id, Organism{
            name:         msg.name,
            planet:       msg.planet,
            intelligence: msg.intelligence,
            owner:        msg.to,
            mintedAt:     now(),
        });

        emit("organism-minted".asComment());
    }

    receive(msg: TransferOrganism) {
        let org: Organism? = self.organisms.get(msg.tokenId);
        require(org != null, "Token not found");
        require(org!!.owner == sender(), "Not owner");

        let updated: Organism = Organism{
            name:         org!!.name,
            planet:       org!!.planet,
            intelligence: org!!.intelligence,
            owner:        msg.newOwner,
            mintedAt:     org!!.mintedAt,
        };
        self.organisms.set(msg.tokenId, updated);
        emit("organism-transferred".asComment());
    }

    // -----------------------------------------------------------------------
    // Getters
    // -----------------------------------------------------------------------
    get fun totalSupply(): Int {
        return self.nextTokenId;
    }

    get fun getOrganism(tokenId: Int): Organism? {
        return self.organisms.get(tokenId);
    }

    get fun owner(): Address {
        return self.owner;
    }
}
