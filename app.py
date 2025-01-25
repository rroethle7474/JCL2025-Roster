import pandas as pd
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Read the CSV files
    logger.info("Reading CSV files...")
    players_2024 = pd.read_csv('2024-JCL-Player-List.csv')
    import_2025 = pd.read_csv('2025-JCL-Import.csv')
    keepers_2025 = pd.read_csv('2025-JCL-Keeper-Eligible-List.csv')

    # Convert salary columns to numeric, removing currency symbols
    players_2024['2024_Salary'] = pd.to_numeric(
        players_2024['2024_Salary'].replace(r'[\$,]', '', regex=True),
        errors='coerce'
    )
    keepers_2025['24_Salary'] = pd.to_numeric(
        keepers_2025['24_Salary'].replace(r'[\$,]', '', regex=True),
        errors='coerce'
    )
    keepers_2025['25_Salary'] = pd.to_numeric(
        keepers_2025['25_Salary'].replace(r'[\$,]', '', regex=True),
        errors='coerce'
    )

    # Add PlayerId column to keepers_2025
    logger.info("Matching Players with PlayerIds...")
    
    # Create a mapping dictionary from 2024 list using just Player name
    player_id_map = players_2024.set_index('Player')['PlayerId'].to_dict()
    
    # Add PlayerId column to keepers_2025
    keepers_2025['PlayerId'] = keepers_2025['Player'].map(player_id_map)
    
    # Validate 2024 salaries match
    logger.info("Validating 2024 salaries...")
    for idx, keeper in keepers_2025.iterrows():
        if keeper['PlayerId'] is not None:
            player_2024 = players_2024[players_2024['PlayerId'] == keeper['PlayerId']].iloc[0]
            if abs(player_2024['2024_Salary'] - keeper['24_Salary']) > 0.01:  # Using 0.01 to handle floating point comparison
                logger.warning(f"Salary mismatch for {keeper['Player']} ({keeper['PlayerId']}):")
                logger.warning(f"2024 List Salary: ${player_2024['2024_Salary']}")
                logger.warning(f"Keeper List Salary: ${keeper['24_Salary']}")

    # Log players without matches
    unmatched_players = keepers_2025[keepers_2025['PlayerId'].isna()]
    if not unmatched_players.empty:
        logger.warning("\nPlayers without matching PlayerIds:")
        for _, player in unmatched_players.iterrows():
            logger.warning(f"Player: {player['Player']}, Team: {player['Team']}")

    # Now update the 2025 import file using PlayerIds
    logger.info("\nUpdating 2025 import salaries...")
    
    # Initialize all 2025 salaries to 0
    import_2025['2025_Salary'] = 0
    
    # Create a mapping of keeper salaries using PlayerId
    keeper_salary_map = dict(zip(keepers_2025['PlayerId'], keepers_2025['25_Salary']))
    
    # Update salaries for keeper-eligible players
    before_count = (import_2025['2025_Salary'] > 0).sum()
    import_2025.loc[import_2025['PlayerId'].isin(keeper_salary_map.keys()), '2025_Salary'] = \
        import_2025.loc[import_2025['PlayerId'].isin(keeper_salary_map.keys()), 'PlayerId'].map(keeper_salary_map)
    after_count = (import_2025['2025_Salary'] > 0).sum()

    # Format salary column to have 2 decimal places
    import_2025['2025_Salary'] = import_2025['2025_Salary'].round(2)
    
    # Log statistics
    logger.info("\nFinal Statistics:")
    logger.info(f"Total rows in import file: {len(import_2025)}")
    logger.info(f"Players with salary > $0: {(import_2025['2025_Salary'] > 0).sum()}")
    logger.info(f"Players with $0 salary: {(import_2025['2025_Salary'] == 0).sum()}")
    logger.info(f"Updated {after_count - before_count} player salaries")
    
    # Save the final result
    output_file = '2025-JCL-Import-Final.csv'
    import_2025.to_csv(output_file, index=False, float_format='%.2f')
    logger.info(f"\nSuccessfully saved {output_file}")

except Exception as e:
    logger.error(f"An error occurred: {str(e)}")
    raise