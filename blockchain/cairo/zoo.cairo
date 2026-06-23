// Cairo — StarkNet smart contract
// Compile: scarb build
// Deploy:  starknet deploy

#[starknet::contract]
mod IntergalacticZoo {
    use starknet::{ContractAddress, get_caller_address, get_block_timestamp};
    use starknet::storage::{StoragePointerReadAccess, StoragePointerWriteAccess, Map};

    // -----------------------------------------------------------------------
    // Events
    // -----------------------------------------------------------------------
    #[event]
    #[derive(Drop, starknet::Event)]
    enum Event {
        OrganismMinted:     OrganismMinted,
        OrganismTransferred: OrganismTransferred,
    }

    #[derive(Drop, starknet::Event)]
    struct OrganismMinted {
        #[key] token_id: u64,
        #[key] owner: ContractAddress,
        name: felt252,
    }

    #[derive(Drop, starknet::Event)]
    struct OrganismTransferred {
        #[key] token_id: u64,
        from: ContractAddress,
        to: ContractAddress,
    }

    // -----------------------------------------------------------------------
    // Storage
    // -----------------------------------------------------------------------
    #[storage]
    struct Storage {
        owner:            ContractAddress,
        next_token_id:    u64,
        organism_name:    Map<u64, felt252>,
        organism_planet:  Map<u64, felt252>,
        organism_iq:      Map<u64, u8>,
        organism_owner:   Map<u64, ContractAddress>,
        organism_created: Map<u64, u64>,
    }

    // -----------------------------------------------------------------------
    // Constructor
    // -----------------------------------------------------------------------
    #[constructor]
    fn constructor(ref self: ContractState, owner: ContractAddress) {
        self.owner.write(owner);
        self.next_token_id.write(0_u64);
    }

    // -----------------------------------------------------------------------
    // ABI
    // -----------------------------------------------------------------------
    #[abi(embed_v0)]
    impl ZooImpl of super::IIntergalacticZoo<ContractState> {
        fn mint(
            ref self:     ContractState,
            to:           ContractAddress,
            name:         felt252,
            planet:       felt252,
            intelligence: u8,
        ) -> u64 {
            assert(get_caller_address() == self.owner.read(), 'Not authorised');
            assert(intelligence <= 100_u8, 'Intelligence must be 0-100');
            let id = self.next_token_id.read() + 1_u64;
            self.next_token_id.write(id);
            self.organism_name.write(id, name);
            self.organism_planet.write(id, planet);
            self.organism_iq.write(id, intelligence);
            self.organism_owner.write(id, to);
            self.organism_created.write(id, get_block_timestamp());
            self.emit(Event::OrganismMinted(OrganismMinted { token_id: id, owner: to, name }));
            id
        }

        fn transfer(ref self: ContractState, to: ContractAddress, token_id: u64) {
            let current_owner = self.organism_owner.read(token_id);
            assert(current_owner == get_caller_address(), 'Not owner');
            self.organism_owner.write(token_id, to);
            self.emit(Event::OrganismTransferred(OrganismTransferred {
                token_id,
                from: current_owner,
                to,
            }));
        }

        fn get_owner(self: @ContractState, token_id: u64) -> ContractAddress {
            self.organism_owner.read(token_id)
        }

        fn total_supply(self: @ContractState) -> u64 {
            self.next_token_id.read()
        }
    }
}

// ---------------------------------------------------------------------------
// Interface trait
// ---------------------------------------------------------------------------
#[starknet::interface]
trait IIntergalacticZoo<TContractState> {
    fn mint(
        ref self: TContractState,
        to: starknet::ContractAddress,
        name: felt252,
        planet: felt252,
        intelligence: u8,
    ) -> u64;
    fn transfer(ref self: TContractState, to: starknet::ContractAddress, token_id: u64);
    fn get_owner(self: @TContractState, token_id: u64) -> starknet::ContractAddress;
    fn total_supply(self: @TContractState) -> u64;
}
