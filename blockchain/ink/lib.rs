// ink! — Polkadot / Substrate smart contract (Rust)
// Requires: cargo-contract 4.x
// Build: cargo contract build
// Deploy via Contracts UI or polkadot.js

#![cfg_attr(not(feature = "std"), no_std, no_main)]

#[ink::contract]
mod intergalactic_zoo {

    use ink::prelude::string::String;
    use ink::prelude::vec::Vec;
    use ink::storage::Mapping;

    // -----------------------------------------------------------------------
    // Events
    // -----------------------------------------------------------------------
    #[ink(event)]
    pub struct OrganismMinted {
        #[ink(topic)]
        token_id: u64,
        #[ink(topic)]
        owner: AccountId,
        name: String,
    }

    #[ink(event)]
    pub struct OrganismTransferred {
        #[ink(topic)]
        token_id: u64,
        from: AccountId,
        to: AccountId,
    }

    // -----------------------------------------------------------------------
    // Storage
    // -----------------------------------------------------------------------
    #[derive(scale::Decode, scale::Encode)]
    #[cfg_attr(feature = "std", derive(scale_info::TypeInfo, ink::storage::traits::StorageLayout))]
    pub struct Organism {
        pub name:         String,
        pub planet:       String,
        pub intelligence: u8,
        pub owner:        AccountId,
    }

    #[ink(storage)]
    pub struct IntergalacticZoo {
        owner:       AccountId,
        next_id:     u64,
        organisms:   Mapping<u64, Organism>,
        owned:       Mapping<AccountId, Vec<u64>>,
    }

    // -----------------------------------------------------------------------
    // Errors
    // -----------------------------------------------------------------------
    #[derive(Debug, PartialEq, Eq)]
    #[ink::scale_derive(Encode, Decode, TypeInfo)]
    pub enum Error {
        NotOwner,
        TokenNotFound,
        InvalidIntelligence,
        NotAuthorised,
    }

    pub type Result<T> = core::result::Result<T, Error>;

    // -----------------------------------------------------------------------
    // Implementation
    // -----------------------------------------------------------------------
    impl IntergalacticZoo {
        #[ink(constructor)]
        pub fn new() -> Self {
            Self {
                owner:     Self::env().caller(),
                next_id:   0,
                organisms: Mapping::default(),
                owned:     Mapping::default(),
            }
        }

        /// Mint a new organism.
        #[ink(message)]
        pub fn mint(
            &mut self,
            to:           AccountId,
            name:         String,
            planet:       String,
            intelligence: u8,
        ) -> Result<u64> {
            if self.env().caller() != self.owner {
                return Err(Error::NotAuthorised);
            }
            if intelligence > 100 {
                return Err(Error::InvalidIntelligence);
            }
            let id = self.next_id;
            self.next_id = id.saturating_add(1);
            self.organisms.insert(id, &Organism { name: name.clone(), planet, intelligence, owner: to });
            let mut list = self.owned.get(to).unwrap_or_default();
            list.push(id);
            self.owned.insert(to, &list);
            self.env().emit_event(OrganismMinted { token_id: id, owner: to, name });
            Ok(id)
        }

        /// Transfer an organism.
        #[ink(message)]
        pub fn transfer(&mut self, to: AccountId, token_id: u64) -> Result<()> {
            let mut org = self.organisms.get(token_id).ok_or(Error::TokenNotFound)?;
            if org.owner != self.env().caller() {
                return Err(Error::NotOwner);
            }
            let from = org.owner;
            org.owner = to;
            self.organisms.insert(token_id, &org);
            let mut list = self.owned.get(to).unwrap_or_default();
            list.push(token_id);
            self.owned.insert(to, &list);
            self.env().emit_event(OrganismTransferred { token_id, from, to });
            Ok(())
        }

        /// Get organism details.
        #[ink(message)]
        pub fn get_organism(&self, token_id: u64) -> Option<Organism> {
            self.organisms.get(token_id)
        }

        /// Total supply.
        #[ink(message)]
        pub fn total_supply(&self) -> u64 {
            self.next_id
        }
    }
}
