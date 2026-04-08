// Rust / Anchor — Solana Program
// Requires: anchor-lang = "0.29"
// Build: anchor build  |  Deploy: anchor deploy

use anchor_lang::prelude::*;

declare_id!("ZooProgram11111111111111111111111111111111");

// ---------------------------------------------------------------------------
// Program
// ---------------------------------------------------------------------------
#[program]
pub mod intergalactic_zoo {
    use super::*;

    /// Initialise the zoo registry (one per deployer).
    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let registry = &mut ctx.accounts.registry;
        registry.authority = ctx.accounts.authority.key();
        registry.organism_count = 0;
        registry.bump = ctx.bumps.registry;
        msg!("Zoo registry initialised for {}", registry.authority);
        Ok(())
    }

    /// Register a new organism.
    pub fn register_organism(
        ctx: Context<RegisterOrganism>,
        name: String,
        planet: String,
        intelligence: u8,
    ) -> Result<()> {
        require!(name.len() <= 64, ZooError::NameTooLong);
        require!(planet.len() <= 64, ZooError::PlanetNameTooLong);
        require!(intelligence <= 100, ZooError::InvalidIntelligence);

        let registry = &mut ctx.accounts.registry;
        let organism  = &mut ctx.accounts.organism;

        organism.id           = registry.organism_count;
        organism.name         = name.clone();
        organism.planet       = planet.clone();
        organism.intelligence = intelligence;
        organism.owner        = ctx.accounts.authority.key();
        organism.created_at   = Clock::get()?.unix_timestamp;

        registry.organism_count += 1;

        emit!(OrganismRegistered {
            id:           organism.id,
            name,
            planet,
            intelligence,
            owner: organism.owner,
        });

        Ok(())
    }

    /// Transfer ownership of an organism.
    pub fn transfer_organism(ctx: Context<TransferOrganism>, new_owner: Pubkey) -> Result<()> {
        let organism = &mut ctx.accounts.organism;
        require_keys_eq!(organism.owner, ctx.accounts.authority.key(), ZooError::NotOwner);
        organism.owner = new_owner;
        Ok(())
    }
}

// ---------------------------------------------------------------------------
// Accounts
// ---------------------------------------------------------------------------
#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer  = authority,
        space  = ZooRegistry::LEN,
        seeds  = [b"zoo_registry", authority.key().as_ref()],
        bump,
    )]
    pub registry:  Account<'info, ZooRegistry>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
#[instruction(name: String, planet: String, intelligence: u8)]
pub struct RegisterOrganism<'info> {
    #[account(mut, has_one = authority)]
    pub registry: Account<'info, ZooRegistry>,
    #[account(
        init,
        payer  = authority,
        space  = OrganismAccount::LEN,
        seeds  = [b"organism", registry.organism_count.to_le_bytes().as_ref()],
        bump,
    )]
    pub organism:  Account<'info, OrganismAccount>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct TransferOrganism<'info> {
    #[account(mut)]
    pub organism:  Account<'info, OrganismAccount>,
    pub authority: Signer<'info>,
}

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------
#[account]
pub struct ZooRegistry {
    pub authority:      Pubkey,
    pub organism_count: u64,
    pub bump:           u8,
}

impl ZooRegistry {
    pub const LEN: usize = 8 + 32 + 8 + 1;
}

#[account]
pub struct OrganismAccount {
    pub id:           u64,
    pub name:         String,
    pub planet:       String,
    pub intelligence: u8,
    pub owner:        Pubkey,
    pub created_at:   i64,
}

impl OrganismAccount {
    pub const LEN: usize = 8 + 8 + (4 + 64) + (4 + 64) + 1 + 32 + 8;
}

// ---------------------------------------------------------------------------
// Events
// ---------------------------------------------------------------------------
#[event]
pub struct OrganismRegistered {
    pub id:           u64,
    pub name:         String,
    pub planet:       String,
    pub intelligence: u8,
    pub owner:        Pubkey,
}

// ---------------------------------------------------------------------------
// Errors
// ---------------------------------------------------------------------------
#[error_code]
pub enum ZooError {
    #[msg("Name must be ≤ 64 characters")]
    NameTooLong,
    #[msg("Planet name must be ≤ 64 characters")]
    PlanetNameTooLong,
    #[msg("Intelligence must be between 0 and 100")]
    InvalidIntelligence,
    #[msg("Caller is not the organism owner")]
    NotOwner,
}
