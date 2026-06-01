# CoE5 Modding Manual Rules (extracted)

Source: [https://illwinter.com/coe5/coe5modding.html](https://illwinter.com/coe5/coe5modding.html)
Extracted: 2026-06-01T21:07:46.525550+00:00

## Statistics

- Sections: 97
- Commands: 864
- Reference tables: 21
- Examples: 3
- Populum command examples: 557

## Table of Contents

- [Introduction](#_introduction)
  - [General Information](#_general_information)
  - [Mod Mechanics](#_mod_mechanics)
  - [Mod Syntax](#_mod_syntax)
- [Minimal Mod for Steam Workshop](#_minimal_mod_for_steam_workshop)
  - [Files](#_files)
  - [orcking.c5m](#_orcking_c5m)
  - [orcbanner.tga](#_orcbanner_tga)
  - [banner.png](#_banner_png)
  - [coe5ws.txt](#_coe5ws_txt)
- [Mod Info](#_mod_info)
  - [Required Commands](#_required_commands)
  - [Optional Commands](#_optional_commands)
- [Maps](#_maps)
- [Fonts & Translation](#_fonts_translation)
- [Weapon Modding](#_weapon_modding)
  - [Start Commands](#_start_commands)
  - [Basic Commands](#_basic_commands)
  - [Sound & Visuals](#_sound_visuals)
  - [Chained Weapons](#_chained_weapons)
  - [Special Attributes](#_special_attributes)
  - [Weapon Modding Numbers](#_weapon_modding_numbers)
- [Magic Item Modding](#_magic_item_modding)
  - [Start Commands](#_start_commands_2)
  - [Basic Commands](#_basic_commands_2)
  - [Special Commands](#_special_commands)
  - [Copy & Clear commands](#_copy_clear_commands)
  - [Monster Commands for Magic Items](#_monster_commands_for_magic_items)
  - [Magic Item Modding Numbers](#_magic_item_modding_numbers)
- [Monster Modding](#_monster_modding)
  - [Start Commands](#_start_commands_3)
  - [Basic Commands](#_basic_commands_3)
  - [Copy & Clear Commands](#_copy_clear_commands_2)
  - [Attacks](#_attacks)
  - [Combat Spells](#_combat_spells)
  - [Movement](#_movement)
  - [Behavior](#_behavior)
  - [Ritual Power](#_ritual_power)
  - [Monster Spawning](#_monster_spawning)
  - [Terrain Altering](#_terrain_altering)
  - [Shapechanging](#_shapechanging)
  - [Immortality and Other Planes](#_immortality_and_other_planes)
  - [Healing and Sanity](#_healing_and_sanity)
  - [Stealth and Scouting](#_stealth_and_scouting)
  - [Monster Types](#_monster_types)
  - [Mirror Commands](#_mirror_commands)
  - [Income Commands](#_income_commands)
  - [Resistances and other Damage Mitigations](#_resistances_and_other_damage_mitigations)
  - [Special Attributes](#_special_attributes_2)
  - [Monster Modding Numbers](#_monster_modding_numbers)
- [Class Modding](#_class_modding)
  - [Start Commands](#_start_commands_4)
  - [Basic Commands](#_basic_commands_4)
  - [Special Start Location](#_special_start_location)
  - [Starting Units](#_starting_units)
  - [Recruitment List](#_recruitment_list)
  - [Income Modifiers](#_income_modifiers)
  - [Special Attributes](#_special_attributes_3)
  - [Class Modding Numbers](#_class_modding_numbers)
- [Terrain Modding](#_terrain_modding)
  - [Start Commands](#_start_commands_5)
  - [Basic Commands](#_basic_commands_5)
  - [Clear Commands](#_clear_commands)
  - [Special Attributes](#_special_attributes_4)
  - [Terrain Modding Numbers](#_terrain_modding_numbers)
- [Terrain Group Modding](#_terrain_group_modding)
  - [Start Commands](#_start_commands_6)
  - [Basic Commands](#_basic_commands_6)
- [Ritual Modding](#_ritual_modding)
  - [Start Commands](#_start_commands_7)
  - [Basic Commands](#_basic_commands_7)
  - [Clear & Copy Commands](#_clear_copy_commands)
  - [Summoning Commands](#_summoning_commands)
  - [Transformation Commands](#_transformation_commands)
  - [Mastery Commands](#_mastery_commands)
  - [Casting Restrictions](#_casting_restrictions)
  - [Ritual Learning Difficulty](#_ritual_learning_difficulty)
  - [Cost Modifications and Effect Boosts](#_cost_modifications_and_effect_boosts)
  - [Targeting Commands](#_targeting_commands)
  - [Affect Target Location](#_affect_target_location)
  - [Affect Target Unit](#_affect_target_unit)
  - [Special Commands](#_special_commands_2)
  - [Event interaction](#_event_interaction)
  - [AI hints](#_ai_hints)
- [Sound Sample Modding](#_sound_sample_modding)
- [Misc Modding](#_misc_modding)
- [Events](#_events)
  - [Event Start & End](#_event_start_end)
  - [Event Triggers](#_event_triggers)
  - [Event Actions](#_event_actions)
  - [Special Values](#_special_values)
- [Updating a Mod](#_updating_a_mod)

## Commands by Section

### Class Modding > Basic Commands

#### `classabdescr "text"`

Sets the description for the ability section of the class. The text must be on one line. The ^ symbol may be used for paragraph breaks.

#### `classdescr "text"`

Sets the description for the class. The text must be on one line. The ^ symbol may be used for paragraph breaks.

#### `hometerr <terrain nbr>`

Sets the home terrain (home citadel) for the class. This terrain must be a citadel or the player will lose immediately when the game begins. This command is mandatory for a new class.

#### `setclassname "class name"`

Sets name for the class (e.g. "Dwarf Queen" or "Necromancer" or “Baron”) This command must be the first command after creating a new class.

### Class Modding > Income Modifiers

#### `goldbonus <percent>`

Percentage bonus to gold income. For example, a bonus of 25 means that the class will have a 25% bonus on all gold income like the Baron.

#### `ironbonus <percent>`

Percentage bonus to iron income. For example, a bonus of 25 means that the class will have a 25% bonus on all iron income like the Baron.

#### `tradebonus <percent>`

Percentage bonus to trade income. For example, a bonus of 50 means that the class will have a 50% bonus on all trade income like the Senator.

### Class Modding > Recruitment List

#### `addcomrec "monster name" <chance> <gold> <gold die> <iron>`

Adds a commander to recruitment list.

#### `addmercrec "monster name" <chance> <nbr> <gold> <gold die> <iron>`

This command works like addunitrec, but the recruitment is mercenary and listed in green color. Mercenaries can only be recruited once and do not count against recruitment limits.

#### `addunitrec "monster name" <chance> <nbr> <gold> <gold die> <iron>`

Adds a monster to the recruitment list for the active class. The chance is a percentage chance that this unit can be recruited each month. The gold die is an open ended die that will be added to the base gold cost of the unit.

#### `clearrec`

Clears the recruitment list for the active class.

#### `humancost <value>`

cost multiplier (100=normal) for human recruitment at special locations (castles, desert palaces), 999=impossible

#### `libbonusdescr "text"`

This text will be shown as a description of the bonus for owning libraries.

#### `libraryrec`

The previous entry in the recruitment list will have increased chance of occurring, depending on the number of libraries owned.

#### `mercboost <value>`

value 100 = mercs will be twice as frequent, -50 = half as frequent

#### `mercpricemult <value>`

value 2 = mercs will be twice as expensive

#### `nostdtroops`

Standard troops are not available to the class.

#### `recasschance <chance>`

This command sets an absolute value for the chance for recruitment offers from human assassins. The default value is 2.

#### `recherochance <chance>`

This command sets an absolute value for the chance for recruitment offers from human heroes. The default value is 1.

#### `reclimiter "string"`

This will alter the requirements for the last added recruitment. string can be something like "+Baron" to require a Baron, "-Baron" to require the Baron to not be alive or "=Dwarf Worker" to require dwarf workers to be upgraded into the new troops.

#### `recterr <terrain nbr>`

The previous entry in the recruitment list can only be recruited in this terrain.

#### `recwizchance <bonus>`

This command sets an extra chance for recruitment offers from human wizards. The default value is 0.

#### `recxcost <resource type> <amount>`

The previous entry in recruitment list will get an additional cost of a special resource (not gold or iron). See table Resource Types for resource types.

See also: `restypes`

#### `stdtroops`

Adds standard troops to recruitment list. Standard troops are spearmen, swordsmen,
archers, crossbowmen, heavy infantries and catapult. Standard troops also include the chance of recruitment offers from Captain (20%) and Scout (10%).

#### `templebonusdescr "text"`

This text will be shown as a description of the bonus for owning temples.

#### `templerec`

The previous entry in the recruitment list will have increased chance of occurring, depending on the number of temples owned.

#### `townbonusdescr "text"`

This text will be shown as a description of the bonus for owning towns.

### Class Modding > Special Attributes

#### `aiclass <value>`

-1=AI players will never get this class by random choice, 0=normal, 1=this class can only be played by AI players

#### `classcitterr <terrain nbr>`

Can also use this terrain as citadels. There can only be one classcitterr per class, but it can be combined with the 3 previous commands.

#### `classforestcit <0-1>`

Can use ancient forests as citadels, like the Troll King.

#### `classminecit <0-1>`

Can use mountain mines as citadels, like the Dwarf Queen.

#### `classtune <sound>`

Sets the class specific tune to this sound number. Tune sound numbers are 125-150 (class specific tunes) and 155-168 (general tunes).

#### `classwoodencit <0-1>`

Can use watch towers as citadels, like the Senator.

#### `otherplanar`

Will enable the class to survive without owning a citadel in Elysium. Note that all classes will survive when owning their start citadel, even if it is not in Elysium.

#### `reqterr <terrain nbr>`

The class requires at least one square of this terrain to be present on a map to play. This must be a terrain type that is normally present on maps. There can only be one reqterr per class.

### Class Modding > Special Start Location

#### `addstartterr <terrain nbr>`

Adds extra terrain types that the class starts with when the game begins, such as extra farms, hamlets or mines.

#### `clearstartterr`

Clears the starting terrain list for the class. This means any additional farms, hamlets, mines etc that the class would start the game with.

#### `createcit <terrain nbr>`

This is the citadel terrain for classes with a different start plane.

#### `likescoast <value>`

A value from -10 to 10 indicating the willingness to start near the coast.

#### `likesnorth <value>`

A value from -10 to 10 indicating the willingness to have a northern start location.

#### `likessouth <value>`

A value from -10 to 10 indicating the willingness to have a southern start location.

#### `startplane <plane>`

Starting citadel should be on this plane. If you use this command you should also use the "createcit" command and the terrain set as hometerr should be set to a gateway/pit/spire terrain. The hometerr terrain will be created in Elysium as a portal to the other plane.

### Class Modding > Start Commands

#### `newclass`

Creates a new class. The new class is automatically assigned a class number from the range of free numbers.

#### `selectclass <class nbr>`

Selects the class to be modified. The selected class is referred to as the active class. Class numbers are listed in Table Class numbers .

See also: `classes`

### Class Modding > Starting Units

#### `addstartcom "monster name"`

Adds a starting commander to the class. All starting units added after the commander will appear already assigned to that commander’s squad at the beginning of the game. The main commander should not be added as a startcom.

#### `addstartunits "monster name" <nbr>`

Adds <nbr> monsters to the starting army for the class. Use this command multiple times to assign several different types of monsters (for example spearmen and archers).

#### `clearstartunits`

Clears the starting army for the active class.

#### `setmaincom "monster name"`

Sets the main commander for the class. For example, the main commander for the Baron class is Baron and the main commander for the Barbarian class is Barbarian Leader. If the main commander does not appear in the recruitment list for the class, he cannot be replaced if lost.

### Events > Event Actions > Affect target location

#### `alterterrain <terrain nbr>`

changes the terrain of the current location

#### `holdit <0-1>`

1=Any independent units on this square will hold and not move away. This holdit flag is cleared if the square is conquered or if any unit is spawned on it.

#### `killsquare`

kills everyone in target square

#### `namesquare “square name”`

Sets name of square, e.g. “Crab Harbor” or “!2The Old Forest” or “!!The Old Tower”

#### `newunits <player> "monsters"`

also sets target unit

#### `promoteunits <player> <max amount> "from monster" "to monster"`

also sets target unit

#### `removeanimalcorpses <nbr>`

Removes this many animal corpses from target location. Nbr must be a positive value.

#### `removecorpses <nbr>`

Removes this many corpses from target location. Nbr must be a positive value.

#### `removehumanoidcorpses <nbr>`

Removes this many humanoid corpses from target location. Nbr must be a positive value.

### Events > Event Actions > Affect target unit

#### `changeowner <player>`

changes ownership of unit to this player

#### `comname "commander name"`

Gives a new name to the target unit. Only works if the target is a commander.

#### `cureoneaff`

Cures one affliction.

#### `gainxp <xp>`

Gives XP to the target unit. XP can be negative to remove XP.

#### `killunit <dmg>`

Hits the target unit with this amount of damage. Use 9999+ for a purge that will disregard any special abilities the target might have (including immortality).

#### `makeaff <aff>`

Gives an affliction to target unit. See table Special Afflictions .

See also: `aff`

#### `makeben <ben>`

Gives a special benefit to target unit. See table Special Benefits . (New for version 5.16)

See also: `ben`

#### `makeblind`

Makes target unit blind.

#### `makediseased`

Makes target unit diseased.

#### `makeminoraff`

Gives a random minor affliction to target unit.

#### `makenhwound`

Gives target unit a never healing wound.

#### `makestationary`

Makes target unit stationary on world map.

#### `newitem "item name"`

Gives a specific magic item to the target unit.

#### `promote <commanderize> "monster"`

commanderize 0 = do not alter commander status, 1 = turns a non commander into a commander

#### `randitem <rare chance>`

Gives a random magic item to the target unit. Rare chance is the chance of being eligible for a rare magic item. It will always be an item that the target unit has appropriate equipment slots for.

#### `randmisc <rare chance>`

Gives a random magic misc item to the target unit. Rare chance is the chance of being eligible for a rare magic item.

### Events > Event Actions > Basic actions

#### `addresources <player> <resource type> <amount>`

Adds an amount of resources to a player. See table Resource Types for resource types.

See also: `restypes`

#### `message <to player> "text"`

Sends a text message to a player.

### Events > Event Actions > Change where the target location is

#### `randloc <planenr> <terr nbr>`

Move target location to a random location. See table Plane Numbers . The plane special values -1 (all planes) and -2 (Elysium-near planes) can also be used. Negative terrain numbers can also be used for special group of terrains. Cannot be used on squareevents.

See also: `planes`

#### `scatterloc <radius>`

Makes target location deviate a bit, can result in the same square. Cannot be used on squareevents.

#### `setloc <x> <y>`

Move target location to a fixed location. Cannot be used on squareevents.

#### `targunitloc`

Set target location to the place where the target unit is.

### Events > Event Actions > Set variables

#### `addvar <var> <value>`

var = 0-9999, adds a value to a variable

#### `copyvar <var1> <var2>`

var = 0-9999, copies variable 1 to variable 2

#### `setvar <var> <value>`

var = 0-9999, sets a variable to a value

### Events > Event Start & End

#### `endevent`

All events must end with this command

#### `playerevent`

Once for each player every turn, occurs in home citadel by default

#### `squareevent`

For each player and each square in the world every turn

### Events > Event Triggers

#### `+aiplayer <player>`

True if this player is an AI player. Only real AI players are valid, not the different independent factions.

#### `+armyowner <player>`

True if square is occupied by this player.

#### `+chance <percent>`

Trigger has percent chance of being true.

#### `+class <player> "class name"`

True if this player is this class.

#### `+hasaffunithere <player> <aff>`

True if player has a unit in the current square that has all the afflictions in the aff mask. See table Special Afflictions . Also sets target unit (player -1 = any player)-

See also: `aff`

#### `+hascom <player> "commander’s name"`

Also sets target unit.

#### `+hascomhere <player> "commander’s name"`

Also sets target unit.

#### `+hasitem <player> "item name"`

True if player has this kind of magic item somewhere in the world. Also sets target unit to wielder (player -1 = any player)

#### `+hasitemhere <player> "item name"`

True if player has this kind of magic item in current square. Also sets target unit to wielder (player -1 = any player)

#### `+hasunit <player> "monster name"`

True if player has this kind of unit somewhere in the world. Also sets target unit (player -1 = any player)

#### `+hasunithere <player> "monster name"`

True if player has this kind of unit at current square. Also sets target unit (player -1 = any player)

#### `+humanplayer <player>`

True if this player is a human player (not an AI player).

#### `+minanimalcorpses <nbr>`

True if at least this many animal corpses (of any type) are present in the square.

#### `+mincorpses <nbr>`

True if at least this many corpses of any type are present in the square.

#### `+minhumancorpses <nbr>`

True if at least this many human corpses are present in the square.

#### `+minhumanoidcorpses <nbr>`

True if at least this many humanoid corpses (humans, hoburghers, giants) are present in the square.

#### `+minturnnbr <turn nbr>`

True if the current turn number is this turn nbr of greater.

#### `+ownsloc <player> <terr nbr>`

True if player owns this terrain anywhere in the world.

#### `+ownsloctarg <player> <terr nbr>`

True if player owns this terrain anywhere in the world. Also sets target location to this place.

#### `+plane <planenr>`

True if target square is on this plane. See table Plane Numbers . The special values -1 (all planes) and -2 (Elysium-near planes) can also be used.

See also: `planes`

#### `+player <player>`

True if current player has this player number.

#### `+season <0-3>`

0=summer, 1=autumn, 2=winter, 3=spring.

#### `+seasondelay <1-3>`

3=early (guaranteed to only happen once per season, 2=mid, 1=late).

#### `+squareactivated`

True if active square is in its activated state. Terrains like Stone Henges can be (de)activated and their status can be checked with this trigger.

#### `+squarename “square name”`

True if square has this name. e.g. “Crab Harbor” or “The Old Tower”

#### `+squareowner <player>`

True if target square is owned or occupied by this player.

#### `+terrain <terr nbr>`

True if target square is of this terrain.

#### `+turnnbr <turn nbr>`

True if the current turn number is this turn nbr. Games start at turn 0 and any turn 0 events are executed before each player can player their first turn. But events are also run once before the game has started for anyone at turn -1.

#### `+varequal <var> <value>`

var = 0-9999, true if variable equals value.

#### `+vargreater <var> <value>`

True if the variable is greater than value.

#### `+varlesser <var> <value>`

True if the variable is less than value.

#### `+varvarequal <var1> <var2>`

var = 0-9999, true if variable 1 equals variable 2.

#### `+varvargreater <var1> <var2>`

var = 0-9999, true if variable 1 is greater than variable 2.

#### `+varvarlesser <var1> <var2>`

var = 0-9999, true if variable 1 is lesser than variable 2.

### Fonts & Translation

#### `fontfile <font nbr 0-2> "fontfile.ttf"`

The filename of the font. Font nbr 0 = standard, 1 = fancy (used for headers), 2 = long texts (for descriptions).

#### `translation "from" "to"`

Translates all occurances of the "from" text to the "to" text.

### Magic Item Modding > Basic Commands

#### `descr "item description"`

Not necessary, as most magic items don’t have descriptions.

#### `itemwep "weapon name"`

Sets the weapon stats of the magic item to those of the weapon with this name. Only use this together with type 1 magic items.

#### `name "item name"`

Set the name of the magic item. Not necessary if you created a new one with newitem.

#### `rarity <rarity>`

Sets how easy it should be to find this item. 0=common, 1=rare, 2=rare & unique, 3=impossible to find as a random item. Default is 0.

#### `spr "image.tga"`

Sets the sprite for the magic item. It should be centered in a 32x32 or 64x64 pixel large image. The drawn item should not be larger than 40x40 pixels however, so if put in a 64x64 image it should be surrounded by black.

#### `type <item type>`

Sets the magic item type. Default is 7 = misc item. See table Magic Item Types

See also: `itemtypes`

### Magic Item Modding > Copy & Clear commands

#### `copyspr "item name"`

Uses the sprite from this magic item.

#### `copystats "item name"`

Copies all stats except the name from this magic item.

### Magic Item Modding > Special Commands

#### `armor <value>`

Armor value, default 0.

#### `combatspell <mode> "spell name"`

Mode -1 = spell will be auto cast on the first round, 1 = unit can cast this spell (like a wand), 2 = spell will be auto cast each round. The spell name is simply the name of the combat spell to be cast, e.g. "Fireball".

#### `combatsum <mode> "summoning string"`

Mode -1 = will summon on the first round of combat, 1 = will summon on all rounds of combat. Summoning string is very similar to the summoning strings used for ritual summoning. E.g. "2d4*Deer & 2*wolf" would summon 2-8 deer and 2 wolves. Commanders cannot be summoned in battle.

#### `hp <value>`

Hit Point bonus, default 0.

#### `protection <value>`

Protection bonus, default 0.

### Magic Item Modding > Start Commands

#### `newitem "item name"`

This command creates a new magic item.

#### `selectitem "item name"`

Selects an existing magic item for modification.

### Maps

#### `mapfile "mapfile.coem"`

The filename of the map. A single mod can contain many maps.

### Misc Modding

#### `playercolor <player> <red> <green> <blue>`

Sets the default color for a player. Each color value is between 0 and 255.

### Mod Info > Optional Commands

#### `modprio <prio 1-9>`

Sets when this mod should be loaded in relation to other mods. Default is 5 and lower numbers are loaded first. Usually you don’t need to use this command.

### Mod Info > Required Commands

#### `description "text"`

A text description of the mod.

#### `icon "image.tga"`

Icon shown when selecting the mod in CoE5. It should be a 256*64 large TGA or PNG image.

### Monster Modding > Attacks

#### `assassinweapon <dmg> "weapon"`

Equips the monster with an assassination weapon of this name that has a base damage of <dmg>. This weapon will be used to make an assassination attempt on an enemy before normal combat (including siege weapons) begins. Assassination attempts can only be used by the attacker and cannot be used against summoned creatures the summoner fails to control.

#### `meleeweapon <dmg> "weapon"`

Equips the monster with a melee weapon of this name that has a base damage of <dmg>.

#### `meleeweapon50s <dmg> "weapon"`

Equips the monster with a melee+skip attack that has 50% chance of being used. If it is used the next attack will  be skipped.

#### `meleeweaponbonus <dmg> "weapon"`

Equips the monster with a melee weapon of this name that has a base damage of <dmg>. This weapon will be used in addition to any other attacks the monster has.

#### `meleeweaponlong <dmg> "weapon"`

This command is deprecated and should no longer be used.

#### `meleeweaponspec <dmg> "weapon"`

Equips the monsters with a special melee weapon. Any normal melee attacks after this one will not be used if this attack was used. Normally used for lances.

#### `prebatweapon <dmg> "weapon"`

Equips the monster with a prebattle effect weapon of this name that has a base damage of <dmg>. This weapon will be used before any normal combat (including assassination) begins.

#### `rangedweapon <dmg> "weapon"`

Equips the monster with a ranged weapon of this name that has a base damage of <dmg>.

#### `rangedweapon25 <dmg> "weapon"`

Equips the monster with a ranged weapon of this name that has a base damage of <dmg>. This weapon has a 25% chance of being used in melee combat.

#### `rangedweapon50 <dmg> "weapon"`

Equips the monster with a ranged weapon of this name that has a base damage of <dmg>. This weapon has a 50% chance of being used in melee combat.

#### `rangedweapon50s <dmg> "weapon"`

Equips the monster with a range+skip weapon that has 50% chance of being used in melee (100% at range). When used the next weapon will be skipped.

#### `rangedweapon50x <dmg> "weapon"`

Equips the monster with a range+skip weapon that has 50% chance of being used in melee or range. When used the next weapon will be skipped.

#### `rangedweaponbonus <dmg> "weapon"`

Equips the monster with a ranged weapon of this name that has a base damage of <dmg>. This weapon will be used in addition to any other attacks the monster has.

#### `siegeweapon <dmg> "weapon"`

Equips the monster with a siege weapon of this name that has a base damage of <dmg>. This weapon will be used in locations that allow sieges, like cities and castles. Siege weapons are used in the first ten rounds of combat before any normal attacks are made.

### Monster Modding > Basic Commands

#### `armor <nbr>`

This command sets the monster’s armor value, which represents its natural protection or the armor it is wearing. Normal human troops have an armor value of 0. Medium armored human troops have an armor value of 1. Heavily armored human troops like Heavy Infantry have an armor value of 2 and very heavily armored troops like Knights and High Lords have an armor value of 3. Extremely tough monsters like dragons may have an armor value of 4 or more.

#### `descr "text"`

Description of the monster. The ^ character will be replaced with a newline.

#### `hp <nbr>`

The maximum number of hit points for the monster. A normal human soldier has 6 hit points and an elite heavily armored soldier has 10 hit points. An ogre has 25 hit points, a troll has 56 hit points and giants, dragons and other huge monsters can have well over a 100 hit points.

#### `mor <nbr>`

The morale of the monster. A normal human soldier has a morale of 4, an elite human soldier has 5 or 6 and powerful monsters can have a morale of 8 or more. Very fearless monsters may have a morale of 15. Setting the morale to 99 makes the monster Mindless and it will be completely unaffected by fear or any other effects that influence morale.

#### `mr <nbr>`

The magic resistance of the monster. Animals have a magic resistance of 2, a normal human has 4 and a more susceptible human has 3. Apprentice mages have a magic resistance of 6, full mages have 8 and master mages have 9. Some highly magical beings may have even higher magic resistance and they can almost never be affected by magic that is resistible.

#### `name "monster name"`

This command renames an existing monster. It is not needed when creating a new monster.

#### `rank <nbr>`

Sets the default deployment rank for the monster. -1 = back, 0 = mid, 1 = front

#### `spr1 "image.tga"`

The file name of the normal image for the monster. This command sets the attack sprite to this image as well.The image should be 32x32 or 64x64 for normal sized monsters and 128x128 for huge monsters. A human being should be about 34 pixels tall and there should be 2 pixels of free space between his feet and the bottom of the image.

#### `spr2 "image.tga"`

The file name of the attack image for the monster. If this is not set, then spr1 will be used for this image too. This command must come after the spr1 command.

#### `str <nbr>`

The strength of the monster. A normal human soldier has a strength of 4, an elite human soldier has 5, a troll has 8 or 9 and giants and dragons have 10 to 12.

### Monster Modding > Behavior

#### `aggressive`

Likes to attack enemies.

#### `ancforest1`

Loves ancient forests.

#### `celwander <objective>`

Only wander if owned by Celestials

#### `celwander2 <objective>`

Try to fulfill this objective if the first one was not possible

#### `coastal`

Loves the coast, like a giant crab.

#### `deadforest1`

Loves dead forests.

#### `deadforest2`

Likes dead forests.

#### `desert1`

Loves deserts.

#### `desert2`

Likes deserts.

#### `desert3`

Hates deserts.

#### `followstupid`

Doesn’t move independently, but follows other stupid units.

#### `forest1`

Loves forests (including ancient forests).

#### `forest2`

Likes forests (including ancient forests).

#### `gates1`

Loves gateways.

#### `hadeswander <objective>`

Only wander if owned by Hades

#### `hadeswander2 <objective>`

Try to fulfill this objective if the first one was not possible

#### `hatesterr <terrain nbr>`

Hates this terrain. Can only be one of these commands per monster and terrain nbr cannot be zero.

#### `horror`

Likes to kill sentient people, also isn’t scared of the void.

#### `indwander <objective>`

Only wander if owned by Independents

#### `infwander <objective>`

Only wander if owned by Inferno

#### `infwander2 <objective>`

Try to fulfill this objective if the first one was not possible

#### `jungle1`

Loves jungles.

#### `jungle2`

Likes jungles.

#### `likesterr <terrain nbr>`

Likes this terrain. Can only be one of these commands per monster and terrain nbr cannot be zero.

#### `loner`

Moves independently of the player and not in groups.

#### `lovesterr <terrain nbr>`

Loves this terrain. Can only be one of these commands per monster and terrain nbr cannot be zero.

#### `maptele`

Can teleport on world map when it is a wandering monster.

#### `maxsinners <value>`

Will gather sinners when owned by Inferno (value=amount before returning)

#### `mines1`

Loves mines.

#### `money1`

Loves gold producing squares.

#### `money2`

Likes gold producing squares.

#### `mountain1`

Loves mountains.

#### `mountain2`

Likes mountains.

#### `nonruin1`

Loves stuff that can be turned into ruins, but is not yet a ruin.

#### `north1`

Loves the north.

#### `pickupanimals <0-1>`

Picks up all animals in the same square and brings them along.

#### `semistupid`

Will move automatically like an independent units unless it is controlled by a player commander.

#### `south1`

Loves the south.

#### `south2`

Likes the south.

#### `stray`

Can stray away from loved and liked terrains.

#### `stupid`

Cannot be controlled by players and will move automatically like an independent unit.

#### `swamp1`

Loves swamps.

#### `swamp2`

Likes swamps.

#### `temple1`

Loves temples.

#### `temple2`

Likes temples.

#### `void2`

Likes the void.

#### `wander <objective>`

Will try to fulfill an objective if it is a commander. See table Objectives for possible values.

See also: `objectives`

#### `wander2 <objective>`

Try to fulfill this objective if the first one was not possible

#### `wanderattack <player number>`

Pause wander to attack this faction if adjacent (-1=all factions, -2=player factions)

#### `wandermaxdist <value>`

Maximum distance for raid missions for wanderers. Dragons have about 6 in this ability.

#### `wanderrest <chance>`

A chance for wandering monsters to rest a turn instead of going on a mission. Dragons have about 85 in this ability.

#### `winteridle`

Monster will not move in the winter if it is in a cold part of the map.

### Monster Modding > Combat Spells

#### `more1spells <nbr>`

The monster starts with more or fewer level 1 spells when it spawns.

#### `more2spells <nbr>`

The monster starts with more or fewer level 2 spells when it spawns.

#### `more3spells <nbr>`

The monster starts with more or fewer level 3 spells when it spawns.

#### `spellrange <value>`

Value = +range for battle spells

#### `spellweapon <path> <level>`

Equips the monster with a Cast Spell weapon in the magic path specified. This spell weapon only has a 25% chance of being successfully used in melee combat.

#### `spellweapon50 <path> <level>`

Equips the monster with a limited Cast Spell Weapon in the magic path specified. This spell weapon has only a 50% chance of being used on any given combat round.

#### `spellweapon50s <path> <level>`

Equips the monster with a limited Cast Spell+skip weapon in the magic path specified. This spell weapon has only a 50% chance of being used on any given combat round. If it is used the next weapon will be skipped.

#### `spellweaponbonus <path> <level>`

Equips the monster with a bonus Cast Spellweapon in the magic path specified. This spell weapon can be used in melee without penalty.

#### `spellweaponsingle <path> <level>`

Equips the monster with a limited Cast Spell Weapon in the magic path specified. Only one of the single spell weapons will be used per combat round if the monster has several

### Monster Modding > Copy & Clear Commands

#### `clearmove`

Removes all movement attributes from the active monster.

#### `clearspec`

Removes all special abilities from the active monster. The special abilities are things like Fire Immunity, Regeneration, etc. This command does not clear movement abilities. Use the clearmove command for that.

#### `clearweapons`

Removes all weapons from the active monster.

#### `copyspr "monster name"`

Copy the sprite of another monster.

#### `copystats "monster name"`

Copies the attributes, weapons, graphics and other properties of the specified monster. The command does not copy the name of the monster, however.

### Monster Modding > Healing and Sanity

#### `coldheal <value>`

heals value hp/month when it’s cold

#### `eatvillage <0-1>`

1 = can eat a village to restore sanity, like a vampire.

#### `fastheal`

A fast healing unit will be fully recovered from any non-fatal damage in at most two months.  Battle afflictions are also healed, but it can take a few more months.

#### `healonterr <terrain nbr>`

Will heal faster when located on this terrain, will also heal monsters with noheal.

#### `minorstartaff <chance>`

Chance of starting with a minor affliction. Chances >100 can give more than one affliction.

#### `noheal`

Monster never heals.

#### `regeneration`

A unit with regeneration will heal 5 percent of its hit points each combat round until it is killed.  Battle afflictions are also healed, but they will take at least one month to heal.  A regenerating creature that is killed will continue to regenerate unless its negative hit points are more than half of its maximum hit points.",

#### `saner <value>`

regains this amount of sanity per month

#### `startinsanity <value>`

Commanders will start with about this much insanity. It has no effect on non-commanders.

#### `varregen <value>`

Like regeneration, but this many percent per round instead of 5.

#### `voidsanity <value>`

reduces insanity gains (like armor)

### Monster Modding > Immortality and Other Planes

#### `banishsurv`

This monster will be flung to another plane when banished, instead of being destroyed.

#### `hadesres <value>`

resistance to the effects of hades

#### `homeplane <plane nbr>`

Other Planar Immortality. Will return to this plane if slain outside it and be indep controlled again.

#### `immortal`

The monster is immortal on its home plane. This command should not be used for beings with Other Planar Immortality.

#### `immortalap <nbr>`

AP cost of reforming its body after dying.

#### `noplanecamo <plane nbr>`

does not use fx_lookslike when in plane = value

#### `planeshift <plane nbr>`

can go to/from other plane, 1=hades, 2=inferno

#### `primable <value>`

By default all animals can be made into primal animals. -1 = monster cannot be turned into a primal variant, 1 = can be turned into a primal variant.

#### `primal <value>`

1 = this monster can be summoned by "Call Primal Being".

#### `primifier <value>`

Will turn this number of animals into primal animals each month.

#### `reformdestroy <value>`

chance to destroy location on immortality respawn (default 0)

#### `reformloc <terrain nbr>`

respawn terrain for immortals (-1 = anywhere, 1000=home)

#### `revertowner <player number>`

Monster will revert to being owned by this faction after its player owner has been defeated. Use player number 24 to revert to a standard independent.

### Monster Modding > Income Commands

#### `fungi <nbr>`

Gives extra income per month of this resource.

#### `gold <nbr>`

Gives extra income per month of this resource.

#### `goldbonus <percent>`

Percentage bonus to gold income for entire nation.

#### `goldcarrier <value>`

spoils of war when defeating this monster.

#### `hands <nbr>`

Gives extra income per month of this resource.

#### `herbs <nbr>`

Gives extra income per month of this resource.

#### `iron <nbr>`

Gives extra income per month of this resource.

#### `ironbonus <percent>`

Percentage bonus to iron income for entire nation.

#### `ironcarrier <value>`

spoils of war when defeating this monster.

#### `lairgoldpen <value>`

Gold inc penalty in percent for this monster’s lair.

#### `lifeforce <nbr>`

Gives extra income per month of this resource.

#### `limitgold <value>`

value = amount of gold per month, but max the value of the square

#### `limitiron <value>`

value = amount of iron per month, but max the value of the square

#### `limittrade <value>`

value = amount of extra trade per month, but max the original trade value of the square.

#### `localgoldbonus <percent>`

att% bonus to gold income in this square (only works in mines)

#### `localironbonus <percent>`

att% bonus to iron income in this square (only works in mines)

#### `relics <nbr>`

Gives extra income per month of this resource.

#### `trade <nbr>`

Gives this number of extra trade points

#### `tradebonus <percent>`

Percentage bonus to trade income for entire nation.

#### `weed <nbr>`

Gives extra income per month of this resource.

### Monster Modding > Mirror Commands

#### `mirror <value>`

1=is small mirror, 2=is large mirror, 3=silver, 4=gold

#### `mirrorammo <value>`

default number of images for this type of mirror (def 20)

#### `phantasm <value>`

1=phantasmal warrior, 2=phantasmal animal, etc.

#### `releasephant <value>`

mirror releases this type of phantasms (has phantasm = value)

#### `releaserate <value>`

bonus to the number of phantasms released

#### `releasespell <value>`

making an attack drains one mirror charge (fx_mirror)

#### `revertmirror <value>`

revert to mirror when empty. 1=small mirror, 2=large mirror, 3=silver, 4=gold

### Monster Modding > Monster Spawning

#### `centspawn <value>`

Bonus for dryad queen auto spawns.

#### `harpyspawn <value>`

Bonus for dryad queen auto spawns.

#### `minospawn <value>`

Bonus for dryad queen auto spawns.

#### `motherspawn <0-7>`

Spawns as one of a few special spawners in the game. 1 = mother of monsters, 2 = teotls of war (spawns d2 jaguars or 1 ozelotls, not on homeplane), 3 = teotls of rain (spawns d3 toad warriors, not on homeplane), 4 = bloody mother (spawns d2 jaguars or d3 serpents, not on homeplane), 5 = teotls of night (spawns d3 bats or 1 ozelotls, not on homeplane), 6 = teotls of underworld (spawns 2d3 longdead, not on homeplane), 7 = teotls of sky (spawns d3 bats or d3 eagle warriors, not on homeplane)

#### `reform <value>`

Value = chance in percent of reforming to previous monster each month (like a slime).

#### `satyrspawn <value>`

Bonus for dryad queen auto spawns.

#### `spawn1d6mon <value>`

Spawns 1d6 of the next monster. value = chance

#### `spawn2d6mon <value>`

Spawns 2d6 of the next monster. value = chance

#### `spawnmon <value>`

Spawns next monster. value/100 = monsters per turn

#### `spawnmonaway <value>`

Spawns next monster, but not on homeplane. value/100 = monsters per turn

#### `spawnoffs <value>`

To spawn something other than the next monster

#### `split <value>`

Value = dmg required in % for splitting into next monster (like a slime).

### Monster Modding > Monster Types

#### `animal`

is an animal

#### `coldblood`

is coldblooded

#### `demonic`

is a demon. Demons are affected by banishment.

#### `dragon <0-2>`

1=dragon, 2=elder dragon.

#### `expendable <0-1>`

Is an expendable unit (can be used payment for certain rituals/recruitments).

#### `female`

is a female

#### `fungus <0-2>`

1 = is a fungus, 2 = is an animated fungus.

#### `goblin <0-1>`

Is an expendable goblin (can be used payment for certain rituals/recruitments).

#### `human`

is a human

#### `inanimate`

is an undead being

#### `kobold <0-1>`

Is an expendable kobold (counts as expendable unit, but comes with a different ability description).

#### `madcultist <0-1>`

Mad cultist might decide to open a gate to Inferno.

#### `primalcult <0-1>`

Primal cultists might decide to open the primal gate.

#### `setcreator <0-1>`

used by monsters that get their name from their creator

#### `ship <0-1>`

Is a ship.

#### `statue <0-1>`

statues get part of their name from their creator, e.g. Statue of Anselm

#### `stonebeing`

monster is made of stone

#### `troll`

is a troll

#### `undead`

is an undead being. Undead beings are affected by banishment.

### Monster Modding > Movement

#### `battlefast`

Monster is fast, but in battles only.

#### `battleslow`

Monster is slow in battles.

#### `battleslow2`

Monster is very slow battles.

#### `desert`

Monster has desert move.

#### `fast`

Monster is fast.

#### `float`

Monster is floating.

#### `flying`

Monster can fly.

#### `huge`

Monster is giant sized. This also makes it a 3x3 square monster on the battlefield.

#### `immobile`

Monster is immobile (cannot move in battle).

#### `mountain`

Monster has mountain move.

#### `noland`

Monster cannot move on land.

#### `passwall`

Monster can move through walls.

#### `shipmove`

Monster is a ship. Movement will cost 1 AP for everyone in the same square.

#### `slow`

Monster is slow on world map.

#### `snow`

Monster has snow move.

#### `stationary`

Monster is stationary (cannot move on world map).

#### `swamp`

Monster has swamp move.

#### `teleport`

Like flying, but the monster will teleport around in combat.

#### `tunnel`

Monster can tunnel on the world map.

#### `wall`

Monster has wall climbing.

#### `water`

Monster can enter water squares.

#### `wateronly`

Same as water & noland. The monster will be aquatic.

### Monster Modding > Resistances and other Damage Mitigations

#### `acidres <value>`

Offers resistance to acid. Value 100 = completely resistant.

#### `affres <value>`

value = chance of not receiving battle affliction

#### `airshield <percent>`

Air Shield with this chance of negating incoming missile attacks.

#### `awe <value>`

Monster has awe. Monsters usually have between 1 to 4 in this ability.

#### `bluntres`

Blunt resistance (half damage).

#### `charmres`

Charm resistance.

#### `coldres <value>`

Offers resistance to cold. Value 100 = completely resistant.

#### `diseaseres`

Disease resistance.

#### `displaced <value>`

25% chance of missing per rank away from target

#### `ethereal`

Is ethereal.

#### `fireres <value>`

Offers resistance to fire. Value 100 = completely resistant.

#### `largeshield`

Equips the monster with a large shield (0-2 protection).

#### `lucky`

Lucky units evade 50% of all attacks.

#### `magicshield`

Equips the monster with a magic shield (0-3 protection).

#### `mirrorimages <value>`

Starts every battle with this amount of mirror images.

#### `nonmaginvul`

Invulnerable to non-magical weapons.

#### `pierceres`

Pierce resistance (half damage).

#### `poisonres <value>`

Offers resistance to poison. Value 100 = completely resistant.

#### `shield`

Equips the monster with a regular shield (0-1 protection).

#### `shockres <value>`

Offers resistance to shock. Value 100 = completely resistant.

#### `slashres`

Slash resistance (half damage).

#### `sleepres`

Sleep resistance.

#### `tangleres <0-1>`

Immunity to tangle vines.

#### `tiny`

Tiny units are missed 50% of the time by normal attacks.

#### `twistfate`

Starts every battle with the Twist Fate buff.

### Monster Modding > Ritual Power

#### `allrit <value>`

knows all rituals of this school (see the Ritual Schools table, -1=all ritual schools)

#### `classcost <nbr>`

to alter cost of all rituals made by this unit, 50=50% more expensive

#### `ctrlchance <nbr>`

Chance of controlling this monster when it is summoned,

#### `gatheranygems`

A commander with this ability will enable the player to gather gems.

#### `gatherfungus`

A commander with this ability will enable the player to gather fungus.

#### `gathergems`

A commander with this ability will enable the player to gather gems of individual types.

#### `gatherhands`

A commander with this ability will enable the player to gather Hands of Glory.

#### `gatherherbs`

A commander with this ability will enable the player to gather herbs.

#### `gatherlifeforce`

A commander with this ability will enable the player to gather lifeforce.

#### `gatherrelics`

A commander with this ability will enable the player to gather relics.

#### `gathersacr`

A commander with this ability will enable the player to gather sacrifices.

#### `gatherweed`

A commander with this ability will enable the player to gather weed.

#### `libmastery <library level>`

For monsters that can level up in a magic library, a value of 2 = magic library or better required, 3 = academy of high magic required. A mastery command is also required on the monster, to determine what monster it will level up to.

#### `mastery <nbr>`

for monsters that can level up, nbr 1=become next monster on leveling, -1=previous monster, etc.

#### `montag <nbr>`

Sets the monster tag value referenced by other modding commands.

#### `power <pow nbr>`

pow nbr 0 means the last created ritual school, -1 = the one before that, etc. Positive numbers are existing ritual powers from CoE5, see the pow nbr table.

#### `rebate <value>`

gives rebate on rituals with fx_rebatefx??

#### `seegems`

A commander with this ability will enable the player to see what type of gems mine produce.

### Monster Modding > Shapechanging

#### `agarthashape <value>`

Will become monster with offset value when on the agartha plane.

#### `aztlanshape <value>`

Will become monster with offset value when on the aztlan plane.

#### `celestialshape <value>`

Will become monster with offset value when on the celestial plane.

#### `elementalshape <value>`

Will become monster with offset value when on the elemental plane.

#### `elysiumshape <value>`

Will become monster with offset value when in Elysium

#### `firstshape <0-1>`

Monster will become next monster if it is slain. Use for main shape of two shape monsters like Oni.

#### `growhp <nbr>`

Monster will grow to the previously created monster if it reaches this amount of HP or more.

#### `growoffs <value>`

To become other than next monster

#### `growterr <terrain nbr>`

The growth will only occur if unit is located in this terrain. Negative terrain numbers can be used.

#### `growtime <value>`

Will grow into next monster after about value turns

#### `hadesshape <value>`

Will become monster with offset value when on the hades plane.

#### `infernoshape <value>`

Will become monster with offset value when on the inferno plane.

#### `landshape <value>`

Will become monster with offset value when on land

#### `primalshape <value>`

Will become monster with offset value when on the primal plane.

#### `secondshape <0-1>`

Monster will revert to previous monster after combat. Use for secondary shape of two shape monsters like Oni.

#### `shrinkhp <nbr>`

Monster will shrink to the next created monster if it reaches this amount of HP or less.

#### `skyshape <value>`

Will become monster with offset value when on the sky plane.

#### `voidshape <value>`

Will become monster with offset value when on the void plane.

#### `watershape <value>`

Will become monster with offset value when in the sea

### Monster Modding > Special Attributes

#### `absorbdead <nbr>`

Can absorb dead and get HP from it. Nbr is the maximum dead absorbed per month. Gains 3 HP/dead.

#### `acidblood <perc>`

AN acid strikeback, 50=50% of incoming damage

#### `aigoldrally <value>`

Hint that AI should go to recruitment loc when having lots of gold

#### `aihold <nbr>`

1 = AI will hold these units in siegable locations and only recruit them there

#### `aimaxshop <value>`

ai won’t buy more than this amount at the same place

#### `ainofollower`

AI hint to always use this commander as a leader (not a subcommander)

#### `aipowcom1 <value>`

unit wants to be led by com with this power at level 1+

#### `aipowcom2 <value>`

unit wants to be led by com with this power at level 2+

#### `aipowcom3 <value>`

unit wants to be led by com with this power at level 3+

#### `airbreather <value>`

This wateronly unit will not drown on land

#### `allitemslots`

Has the full set of item slots.

#### `alone <dmg>`

Will take damage each month another monster of the same type is in the same square.

#### `armytrainer <nbr>`

Units in the same square will get this amount of XP each month.

#### `autoastrology`

Superior Astrologist.

#### `awakenfungus <radius>`

Will awaken nearby mushrooms in combat.

#### `awakentrees <radius>`

Will awaken nearby trees & bushes in combat.

#### `berserker`

Can go berserk.

#### `burnforest <nbr>`

1 = can start forest fires, 100 = auto burns forests.

#### `changetemp <value>`

makes square value degrees hotter

#### `chopforest <value>`

1=can chop down forests.

#### `clumsy`

Misses more than usual (soulless have this ability).

#### `coldaura <dmg>`

AN cold strikeback (std dmg = 2)

#### `combustionaura <radius>`

Puts nearby units on fire

#### `confusionaura <radius>`

Confuses nearby units (easy MR negates)

#### `darkbless <0-1>`

Has the dark blessing of a scourge lord

#### `deepsleeper <value>`

Must receive at least 1-value dmg in one hit to wake up.

#### `defiler <range>`

Needs to drain lifeforce to cast spells, range=max drain range.

#### `deployoutside <0-1>`

setup this unit outside fort in battles. The monster probably needs to be small (1x1 square) and few in numbers for the deployment to work properly, there is not much space left outside the walls before coming too close to the enemies.

#### `desolator <value>`

Drain value lifeforce from current square each month (like scourge lord pillar).

#### `desolcloud <radius>`

Spreads desolation cloud (exhaustion).

#### `digest <dmg>`

Gives this amount of dmg per round to units in stomach.

#### `diseasecloud <value>`

spreads disease cloud, value = radius + 1

#### `diseaseshield <0-1>`

Disease strikeback (MR negates).

#### `dmgonterr <terrain nbr>`

Takes 1 point of dmg per month when in this terrain. A single unit can only have one dmgonterr ability. If it has more than one, only the one highest terrain nbr will take effect.

#### `dmgonterrbonus <value>`

Adds to the damage of the dmgonterr ability

#### `drawsize <percent>`

Draw the unit this amount of percent larger when shown on his unit token. Can be negative for smaller as well. Use this command to easily fine tune the units size to fit nicely in it token. Don’t use any large values as the resizing is not done everywhere in the game.

#### `eatdead <chance>`

Chance of eating a corpse and reproducing.

#### `eatdeadcap <chance>`

Chance of eating a corpse and reproducing, capped at one per square and month.

#### `evasion <0-1>`

25% chance to evade attacks.

#### `extraeyes <nbr>`

Monster has this number of extra eyes. Use -1 to create a cyclops with one eye.

#### `fear <value>`

causes fear: 1=fear, 2=dread, 3=terror

#### `fireaura <dmg>`

Fire strikeback (std dmg = 3)

#### `fireexpl <dmg>`

Fire explosion on death.

#### `forestheart <0-1>`

takes control of nearby forests

#### `frontpos`

Rank+, deploys further towards the front.

#### `holy`

Sacred, takes advantage of bless effects.

#### `hpoverflow <nbr>`

1 = HP overflow is allowed even after the battle.

#### `iceprot <value>`

+value armor in cold climate

#### `incorporate <dmg>`

Steals this amount of HP per round from units in stomach.

#### `indepitem <percent>`

Like randomitem, but only for indeps (all indep nations).

#### `leadership <nbr>`

Gives this amount of extra morale to units under his command.

#### `likestoburn <value>`

value% chance of wanting to burn a forest (wandering indep commanders only)

#### `localleadership <nbr>`

Gives this amount of extra morale to nearby friendly units.

#### `lookslike <offset>`

Offset to monster it looks like. This is used by e.g. werewolves in order to look like some other unit when they are inspected.

#### `makeruin <value>`

value = chance of turning current square into a ruin if possible

#### `maxsum <value>`

the maximum amount that can be summoned in a single battle

#### `meleeambush <value>`

Will start in melee combat when ambushing

#### `melt <value>`

takes value dmg per month when not cold

#### `mindexpl <0-1>`

1 = explodes in Mental Agony on Death

#### `miscslots`

Has only 2 misc slots.

#### `nametype <nametype>`

Sets the type of random name this monster should get. See Table Nametypes .

See also: `nametypes`

#### `neverturn <value>`

never draw facing the other way

#### `nobootslots`

Has no boot slots.

#### `nocombat`

Non combatant, will not participate in combats.

#### `noeyes`

monster has no eyes and needs no eyes to be effective

#### `noleader`

Cannot command any unit even if monster is a commander.

#### `noslots`

Has no item slots at all.

#### `nozoc`

No Zone of Control (castle gates have this ability)

#### `petriaura <range>`

Causes petrification like gorgon

#### `poisonaura <nbr>`

Poison strikeback (std dmg = 4)

#### `poisoncloud <value>`

spreads poison cloud, value = radius + 1

#### `poisonexpl <dmg>`

Poison explosion on death. A giant mushroom has this ability with dmg 10.

#### `poisonspikes <dmg>`

AN poison strikeback

#### `putridexpl <value>`

Putrid cloud upon death (value magic dmg + disease(MR))

#### `randomitem <percent>`

Percent is the chance of the monster starting with a random magic item.

#### `randommisc <percent>`

Percent is the chance of the monster starting with a random magic misc item.

#### `randomrare <percent>`

Monster will start with a random magic item. Percent is the chance of a rare item being allowed.

#### `randomweapon <percent>`

Percent is the chance of the monster starting with a random magic weapon.

#### `reanimate <value>`

reanimates automatically if possible, value = max amount / month

#### `rearpos`

Rank-, deploys further back.

#### `riverdmg <value>`

takes an value damage when passing a river

#### `scourgedefiler <value>`

Needs to drain lifeforce to cast spells of the defilement path, range=max drain range.

#### `scry <nbr>`

Can scry for 3 AP, attr=radius*10 (5=1square, 15=9 squares).

#### `scrycost <nbr>`

Scrying cost this amount of gold.

#### `seduceaura <value>`

attacker within this range might get seduced instead

#### `sensedead <0-1>`

1 = can sense the number of corpses of all types in current square

#### `shardexpl <dmg>`

Shard explosion on death.

#### `shockaura <dmg>`

AN cold strikeback (std dmg = 3)

#### `siegetunnel <chance>`

Chance of emerging inside fort when storming.

#### `sitepopboost <value>`

Will boost indep generation at current site (100 = +100%).

#### `size1x1`

Monster only takes up a single square on the battlefield.

#### `size2x2`

Monster takes up 2x2 squares on the battlefield. (The huge movement ability gives a 3x3 size token on the battlefield).

#### `slavehunt <die>`

Can create slave warriors. The amount of slaves is an open ended die.

#### `sleeper <chance>`

Chance of starting a battle asleep if defending.

#### `slimeshield <0-1>`

Slime strikeback

#### `snowsleeper <chance>`

Chance of starting a battle asleep if defending and it is snowy.

#### `spread <value>`

unit will position itself spread out among the other troops

#### `startitem "item name"`

Starts with this item.

#### `swallowres`

Immune to swallow attacks (used for castle gates).

#### `thrallhunt <value>`

can create thralls (vampire)

#### `trample <dmg>`

Can trample smaller unit for this amount of damage.

#### `tramplexsize <value>`

Extra size regarding trampling. A size one trampling unit needs tramplexsize 1 to be able to trample anyone at all.

#### `transport <value>`

Is a ship and can transport value amount of size 1 units.

#### `treelook`

sprite will be rotated and scaled randomly, like a random tree

#### `tunnelmove <dmg>`

Tunnel teleporting in combat like a Purple Worm.

#### `unaging`

Immune to aging effects like decay.

#### `unimportant`

Battles can be won without killing this unit.

#### `unique <nbr>`

This is a unique monster, there can only be one of it in the entire world.

#### `vassal <0-1>`

Is a vassal knight and will get part of yearly consription.

#### `weaponslots`

Only has weapon and misc slots.

### Monster Modding > Start Commands

#### `newmonster "monster name"`

Creates a new monster. This new monster will be affected by the following modding commands until the next active monster is set. The monster can have the same name as another monster.

#### `selectmonster "monster name" [<offset>]`

Selects the monster that will be affected by the following modding commands. The selected monster is referred to as the active monster. The selectmonster command always selects the first monster of that name in the monster list. If there is more than one monster with the same name (e.g. longdead) the offset value can be used to select them. Leave the offset out if you only want to select the first monster. The default value of the offset is 0. The offset used by this command cannot be set to a negative value, unlike the offset for the lookslike command. Offset value 1 means the command selects the (first + 1) monster of that name, i.e. the second monster. Offset 2 selects the third monster of the same name etc. Note that this command cannot use the "1:spearman" syntax.

### Monster Modding > Stealth and Scouting

#### `acutesenses`

Monster has acute senses.

#### `badsight`

Monster has bad eye sight and will miss 20% of all attacks.

#### `desertstealth`

Monster is stealthy in deserts.

#### `farsight <0-1>`

Can see further on the world map.

#### `foreststealth`

Monster is stealthy in forests.

#### `hideanimals <0-1>`

Animals following this commander gains forest stealth.

#### `invisible`

Monster is invisible.

#### `snowstealth`

Monster is stealthy in snowy locations.

#### `spiritsight`

Monster has spirit sight.

#### `stealth`

Monster is stealthy.

#### `terrstealth <terrain nbr>`

Monster is stealthy in this terrain.

#### `terrstealthinv`

Monster gets invisible instead of just stealthy in the terrstealth terrain.

### Monster Modding > Terrain Altering

#### `colonymsg <value>`

1 = everyone will get a message when a colony is created.

#### `colonyterr <value>`

Terrain to build colonies in (default -87).

#### `makecolony <terrain nbr>`

Has a chance of turning a standard terrain into ‘terr’ and then die.

#### `terraformch <value>`

Chance of terraforming square (default 100).

#### `terraformfrom <value>`

Changes this terrain into something. Use next two commands to setup that and how often.

#### `terraformto <value>`

Terraforms to this terrain (default plain).

### Ritual Modding > AI hints

#### `aialways <chance>`

AI will always (if chance = 100 try to cast this ritual, but not make any long time plans for it. chance=999 is special and means the AI will also make plans for the ritual.)

#### `aiapprspam <chance>`

AI will dedicate apprentices to stay at home and only spam this ritual. Chance is 0-100

#### `aimaxcast <value>`

An AI player will never cast this ritual more than this number of times in a game

#### `ainosimul`

No more than one commander may plan to cast this ritual at once

#### `ainotclose1 <terrain nbr>`

AI will not cast ritual if close to this terrain, radius=1

#### `ainotclose2 <terrain nbr>`

AI will not cast ritual if close to this terrain, radius=2

#### `ainotclose3 <terrain nbr>`

AI will not cast ritual if close to this terrain, radius=3

#### `ainothere <terrain nbr>`

AI will not cast ritual in this terrain

#### `ainotnearhome <mindist>`

AI should not cast this ritual close to home (mindist = nbr of squares away)

#### `aionlyplane <plane nr>`

AI will only cast ritual when on this plane

#### `airare <chance>`

Reduces the chance of the AI trying to use this ritual. Chance is the chance of casting the ritual and can be from 1-99. -1 is a special value meaning never cast it.

#### `airestrig <value>`

AI will always try to cast this ritual if it has at least this many of the primary resource for the ritual

#### `aitarg <value>`

For long range rituals. 1=try to target squares with enemy commanders, 2=try to target valuable squares with corpses in

#### `aiweakonly <troop strength>`

AI commander will only cast this ritual if his troop strength is below this value. One spearman gives 10 troop strength points.

#### `aiwhere <terrain nbr>`

restricts the AI to only cast ritual in this terrain

### Ritual Modding > Affect Target Location

#### `alterloc <terrain nbr>`

Changes target square to this terrain.

#### `centerloc`

Center map on target location.

#### `destroyterr`

Destroys any valuable terrain at target location.

#### `makeportal <portal nbr>`

Connect this square to other portals of the same number. Portal nbr 1000 is special and will create a unique number.

#### `movehome`

Moves home citadel location to target square.

#### `planeswap <plane nbr>`

Swaps target square with corresponding square on this plane.

#### `portalroom <terrain nbr>`

Creates a portal to a location around this terrain.

#### `putcorpses <nbr>`

Creates a number of human corpses in the target square (as if a fight involving humans had taken place there). Add 10000 to nbr in order to make the number of corpses scale with the sacrifice amount used.

#### `reducetown`

Reduces settlement at target location one step in size.

#### `scatterscry <nbr of squares>`

Scry in a scattered way around target location.

#### `scryloc <radius*10>`

Scry in a circle around target location.

#### `squareench <ench nbr>`

Puts an enchantment at target location.

#### `squarespec <ss bitmask>`

Adds special square flags to square. The only useful values are 2^14 (16384) converted to El, 2^16 (65536) poison fog, 2^17 (131072) strange mist.

#### `trollifyloc`

Transform forest at target location into a troll forest.

### Ritual Modding > Affect Target Unit

#### `afftarg <aff nbr>`

Gives an affliction bitmask to the target unit. See table Special Afflictions . (New for version 5.16)

See also: `aff`

#### `bentarg <ben nbr>`

Gives a beneficial bitmask to the target unit. See table Special Benefits . Particularly useful values for rituals are 2^26 to get the twiceborn effect or 2^24 to get the Stygian Bath effect. Note that most ben effects are temporary any will disappear after battle or during the turn and will be useless for rituals.

See also: `ben`

#### `bentargall <ben nbr>`

Like bentarg, but also affects all the target’s followers.

#### `bentargvar <ben nbr>`

Like bentarg, but the unit will only be affected if he is located in the terrain in the generic modding variable.

#### `cureoneaff <chance>`

Has this chance of curing one affliction on the target unit.

#### `fillmirror <images>`

Puts a number of images into a mirror, -1 = fill to default value (mirrorammo)

#### `insanity <value>`

Gives insanity to the target unit. Negative value can be used to cure insanity. Only works if target is a commander.

#### `killtarg <dmg>`

Gives between 1 and <dmg> amount of damage to target unit.  Use a value of  9999 for autokill.

#### `selectfx <fx nbr>`

Sets mod-fx-nbr to this value. Used by next command.

#### `setfx <value>`

Gives target unit a fx of type mod-fx-nbr and sets it to this value.

#### `setvar <nbr>`

Set the generic modding variable to this value.

#### `teleportloc <1-2>`

Teleport target unit to target location. Attribute value 2 means the caster’s entire army is teleported to the target location.

#### `updatehome`

Updates home for target unit to where he stands. This is used to make some immortals resurrect in the correct place.

### Ritual Modding > Basic Commands

#### `cost <resource type> <amount>`

Adds a resource cost to the ritual. E.g. cost 4 10 to add a cost of 10 sacrifices. A single ritual can have at most 4 different costs.  See table Resource Types for resource types.

See also: `restypes`

#### `level <1-9>`

The level of the ritual. Usually the level is between 1 (apprentice level) and 3 (master level).

#### `ritpow <pow nbr>`

Sets the ritpow used. If command is not used, the latest created newritpow will be used. Existing ritpow numbers can be found in the Ritual schools (pow nbr) table.

See also: `pownbr`

#### `terr <terrain nbr>`

Restrict ritual to this terrain only. Negative numbers can be used for special terrain combinations.

### Ritual Modding > Casting Restrictions

#### `benrestrict <ben nbr>`

Caster cannot have this beneficial bitmask

#### `enchherereq <ench nbr>`

This type of Enchantment must be active where there ritual is cast.

#### `eventvarreq <var>`

This event variable must be 1 or higher for ritual to be castable.

#### `fewmonreq <max>`

The monsters in addstring "(-)…​" must not be more than max at current location.

#### `fortreq <fort part>`

There must be a fort with this fort part here.

#### `fxreq <fx nbr>`

Unit must have 1+ in this fx to learn and cast this ritual. This command is probably not useful for modding.

#### `hasportalreq <portal nbr>`

Player must own a portal of this number.

#### `homecitreq < -1 or 1>`

Can only cast this in the player’s home citadel. -1=cannot.

#### `homereq < -1 or 1>`

Caster can only cast this in his home province. -1=cannot.

#### `levelreq <1-9>`

Caster must be exactly this level to use this ritual and cannot have another power at higher level.

#### `maxcast <value>`

Ritual cannot be cast more than this number of times per player

#### `minmonreq <min>`

The monsters in addstring "(&)…​" must be at least 'min' in number at current location.

#### `monplayerreq [<min>]`

At least min number (default 1) of the monsters in addstring "(&)…​" must be in the world and owned by the current player. The min attribute is optional and can be omitted.

#### `monworldreq [<min>]`

At least min number (default 1) of the monsters in addstring "(&)…​" must be in the world. The min attribute is optional and can be omitted.

#### `nearby1req <terrain nbr>`

This terrain must be within 1 square when casting the ritual (a 3x3 square area).

#### `nearby3req <terrain nbr>`

This terrain must be within 3 squares when casting the ritual (a 7x7 square area).

#### `nearby5req <terrain nbr>`

This terrain must be within 5 squares when casting the ritual (a 11x11 square area).

#### `nearby7req <terrain nbr>`

This terrain must be within 7 squares when casting the ritual (a 15x15 square area).

#### `nearby99req <terrain nbr>`

This terrain must be somewhere on the same plane when casting the ritual

#### `noeventvarreq <var>`

This event variable must be 0 or lower for ritual to be castable.

#### `nofortreq <fort part>`

There cannot be a fort with this fort part here.

#### `nofxherereq <fx nbr>`

Cannot be a unit with this fx at the current location.

#### `nomonelysiumreq`

Monsters in addstring "(-)…​" must not be in elysium/sky/agartha. Monster in addstring "(+)…​" will disable following minuses if monster fulfills same requirement. This applies for all nomon… commands.

#### `nomonhomereq`

Monsters in addstring "(-)…​" must not have their home at current location.

#### `nomonmasteryreq`

Monsters in addstring "(-)…​" must not be in the world and owned by the current player unless level is higher than ritual requires

#### `nomonplayerreq [<limit>]`

Monsters in addstring "(-)…​" in the world and owned by the current player must be fewer than limit. Default limit is 1.

#### `nomonreq`

Monsters in addstring "(-)…​" must not be at current location.

#### `nomonworldreq [<limit>]`

Monsters in addstring "(-)…​" in the world must be fewer than limit. Default limit is 1.

#### `nonearby1req <terrain nbr>`

This terrain cannot be within 1 square when casting the ritual (a 3x3 square area).

#### `nonearby3req <terrain nbr>`

This terrain cannot be within 3 squares when casting the ritual (a 7x7 square area).

#### `nonearby5req <terrain nbr>`

This terrain cannot be within 5 squares when casting the ritual (a 11x11 square area).

#### `nonearby7req <terrain nbr>`

This terrain cannot be within 7 squares when casting the ritual (a 15x15 square area).

#### `nonearby99req <terrain nbr>`

This terrain cannot be anywhere on the same plane when casting the ritual

#### `noportalreq <0-1>`

Location where ritual is cast mustn’t contain a portal

#### `planereq <plane nbr>`

Can only be cast on this plane. See table Plane Numbers .

See also: `planes`

#### `resreq <res nbr>`

Caster must have this resistance bitmask.

#### `resrestrict <res nbr>`

Caster cannot have this resistance bitmask. Useful values are 2^4 for undead, 2^20 for immortal and 2^26 for ethereal.

### Ritual Modding > Clear & Copy Commands

#### `clearritspec`

Removes all special attributes from a ritual. This is only useful when modifying existing rituals.

#### `copyritual "name"`

Copies all stats and abilities (except pow nbr and name) from another ritual to the current one.

### Ritual Modding > Cost Modifications and Effect Boosts

#### `apcost <nbr>`

Extra Action Points cost for the rituals.

#### `rebatefx25 <fx nbr>`

Units with this fx nbr get 25% rebate

#### `rebatefx50 <fx nbr>`

Units with this fx nbr get 50% rebate

#### `rebateterr20 <terrain nbr>`

Ritual cost is 20% cheaper in this terrain

#### `rebateterr50 <terrain nbr>`

Ritual cost is 20% cheaper in this terrain

#### `sacrscale`

Summoning amount scales with sacrifice production of target square

#### `terrboost <terrain nbr>`

Adds 1 to number of summoned monsters when done in this terrain

#### `terrscale50 <terrain nbr>`

+50% number of summoned monster when done in this terrain

### Ritual Modding > Event interaction

#### `addeventvar <var>`

increases the value of this event variable by 1

#### `cleareventvar <var>`

set this event variable to 0

#### `seteventvar <var>`

set this event variable to 1

#### `subeventvar <var>`

decreases the value of this event variable by 1

### Ritual Modding > Mastery Commands

#### `forgetrits`

Forgets all known rituals.

#### `gainrit <offset>`

Learns the ritual that is offset numbers away. E.g. offset 1 = learn the following ritual when casting this one.

#### `levelup <1-9>`

Will level up if caster is below this level. Leveling up means becoming a new monster determined by the mastery monster command.

#### `levelupmon <1-9>`

Like levelup, but the new monster type is set by the addstring command. Set the new monster type in the addstring command.

#### `newrit <1-9>`

Grants a new ritual of this level.

#### `newspell1 <path nbr>`

Learns one new level 1 combat spell from this path.

#### `newspell2 <path nbr>`

Learns one new level 2 combat spell from this path.

#### `newspell3 <path nbr>`

Learns one new level 3 combat spell from this path.

#### `rebatelvl <1-9>`

This ritual will be half price if caster is this level or higher.

### Ritual Modding > Ritual Learning Difficulty

#### `afterprev`

must know previous ritual before learning this one

#### `free`

always start with this ritual in addition the others

#### `gathergems`

will start gathering gems when knowing this ritual

#### `nexttoo`

receives next ritual too when receiving this one

#### `nodemon`

demons never know this ritual

#### `nofemale`

females never know this ritual

#### `nostart`

never start with this ritual (or learn from mastery)

#### `notforpoor`

units with more expensive rituals can’t get this one

#### `noundead`

undeads never know this ritual

#### `rarestart`

reduced chance of starting with this ritual

#### `start`

will start with this ritual(s), no others

### Ritual Modding > Special Commands

#### `castertarg`

Sets target unit to caster.

#### `centercaster`

Center map on caster.

#### `closewin`

Closes the ritual window after the ritual has completed.

#### `enchreqterr <terrain nbr>`

Enchantment will be auto dispelled if it is outside this terrain.

#### `failplayer <player nbr>`

Failed summons will be owned by this player.

#### `forgetcurrit`

Caster will forget this ritual after casting it.

#### `gainbless <percent>`

Percent chance of gaining a bless effect.

#### `gaindarkbless <percent>`

Percent chance of gaining a dark bless effect.

#### `ornext <percent>`

This ritual will have one of two possible effects. The first effect will consist of the following command, the next effect will consist of the remaining commands. Percent is the chance of the first effect happening.

#### `ornext2 <percent>`

This ritual will have one of two possible effects. The first effect will consist of the two following commands, the next effect will consist of the remaining commands. Percent is the chance of the first effect happening.

#### `ornext3 <percent>`

This ritual will have one of two possible effects. The first effect will consist of the three following commands, the next effect will consist of the remaining commands. Percent is the chance of the first effect happening.

#### `ornext4 <percent>`

Like the other ornext commands.

#### `ornext5 <percent>`

Like the other ornext commands.

#### `simulacrum`

Creates a simulacrum.

#### `soundfx <sound>`

Play this sound effect.

#### `transformtarg <mode>`

Target unit will be transformed into one of the monsters added by addstring. Normally you want to use mode 1. Mode 2 will transform the units into higher monsters if they have higher skill level than necessary to cast the ritual.

#### `unfollowtarg`

Removes all followers from the target, should he be a commander that is commanding any units.

### Ritual Modding > Start Commands

#### `newritpow`

Creates an entire new school of rituals called a ritpow. This should be the first command when creating a new batch of rituals.

#### `newritual "name"`

Create a new ritual with this name. This should be the first command for each new ritual.

#### `selectritual "name" [<offs>]`

The optional value offs can be used to select a ritual other than the first one with this name. 0=the first one, 1=the second ritual with this name.

### Ritual Modding > Summoning Commands

#### `addstring "string"`

Adds some text data to a ritual. Most often used to set what is summoned by a summoning ritual, but it depends on what effects are in the ritual. All addstring commands will be processed before any other commands for the ritual, so it does not matter where in the ritual you place them.

#### `defctrl <percent>`

Default control chance for summonings. Can be overridden by monster’s own ctrlchance.

#### `farsummon`

Like summoning, but it will occur at target location instead of at the caster’s location.

#### `raiseanimals`

Raises animal corpses from the dead.

#### `raisedead`

Raises humanoid corpses from the dead.

#### `setplayer <player nbr>`

Following summons will be owned by this player. Default owner is the current player. Player -1 resets the owner to the default.

#### `specpow <value>`

Makes a druid summoning, 1=minor, 2=major

#### `sum0chance <percent>`

Use with summonings. Percent = chance of first "string" to be used instead of a random string among the others.

#### `sum0snow <percent>`

Works like sum0chance, but it can only succeed if there is snow at the target location.

#### `sum1chance <percent>`

Use with summonings. Percent = chance of second "string" to be used instead of a random string among the third and later.

#### `sum2chance <percent>`

Same but one higher.

#### `sum3chance <percent>`

Same but one higher.

#### `sum4chance <percent>`

Same but one higher.

#### `summoning`

The ritual will summon the monsters specified in a random "string". Use addstring to add up to 15 strings with monsters. The string should be written like these examples:"1d6*Goblin", "c*Captain & 2d6*spearman & 2d4+2*Archer", "Purple Worm". The c* indicates a commander and 2d6 means two 6-sided dice will determine the number of monsters summoned. Dice cannot be combined with commanders.

#### `varcost <percent>`

Set variable sacrifice amount (50=50-150%, 100=0-150%)

### Ritual Modding > Targeting Commands

#### `choosefxtarg <fx nbr>`

Player will choose a target unit that has this fx nbr.

#### `chooseloc <1-5>`

Player choose target location. 2=deviate to many dead, 3=empty mirror req, 4=empty gold mirror, 5=horror mark deviation

#### `chooseterrloc <terrain nbr>`

Player will choose target location for ritual.

#### `mirrortarg <mirror size>`

Set targ to an empty mirror unit, attr = size for mirror, -1=any size

#### `montarg <1>`

Sets targ unit to a random unit at target location among the type added by addstring.

#### `newlocplanes <terrain nbr>`

Like randnewloc but will go to other planes if necessary (but not hades)

#### `planeloc <plane nbr>`

Shift target loc to same position but on another plane (neg = toggle between this plane and elysium).

#### `randnewloc <terrain nbr>`

Like previous, but try to find an unknown location first.

#### `randomloc <1-5>`

1=random land loc, 2=many dead (excluding present), 3=rand enemy com, 4=rand enemy citadel, 5=home citadel

#### `randterrloc <terrain nbr>`

Sets loc to a random terrain of this type on active plane.

#### `setplane <plane nbr>`

Following randomloc etc. commands will be restricted to this plane

### Ritual Modding > Transformation Commands

#### `promotion <nbr of units>`

Promote existing units to another monster type. Use addstring to add promotion pairs, the first string sets a source unit and the second one the destination units. Multiple of these pairs can be added to a single ritual.

#### `transformtarg <1-2>`

Will transform target into the unit type set by addstring. Value 1 = standard (use this), 2 = transform into following unit if level is high enough.

### Sound Sample Modding

#### `sample <sound> "sample.sw"`

Sets a sample file (sample.sw) as a certain sound effect number (sound). The sound effect number can be between 0 and 249, high numbers (170+) will create new samples and low number will replace the old samples that already occupies those numbers. The sample file should have the .sw (mono) or .sw2 (stereo) extension and be saved as a signed 16-bit 22050 Hz sample.

#### `sampleisloopmusic <sound>`

Turns this sample into one of the background tunes. That means it will loop into another background tune when it has finished playing.

#### `sampleismusic <sound>`

Turns this sample into one a class specific tunes. That means it will loop into a background tune when it has finished playing. If you create a sample as a class specific tune, this must be used on that sample to keep the music playing. If used on a background tune it will remove that tune from the loop of background music.

### Terrain Group Modding > Basic Commands

#### `addallforests`

Adds all different forest terrains to the group. Jungles are not included.

#### `addalljungles`

Adds all different jungle terrains to the group.

#### `addallsettlements`

Adds all different human settlement terrains to the group.

#### `addterr <terrain nbr>`

Adds a terrain to this group. Negative numbers cannot be used here. By default a terrain group is empty.

#### `invert`

Inverts the contents of the group. Very useful when making a group that should contains all terrains but one.

#### `remterr <terrain nbr>`

Removes this terrain from the group.

#### `setname "name"`

Sets the name for the terrain group, e.g. "forests and temples".

### Terrain Group Modding > Start Commands

#### `selectterrgroup <terrgroup nbr>`

Select the terrain group to be modified. The number must be between -1000 and -1199. The numbers between -1 and -999 are reserved for standard CoE5 and cannot be modified.

### Terrain Modding > Basic Commands

#### `apcost <nbr>`

Action Point cost for moving through the terrain.

#### `dead <nbr>`

The location starts with <nbr> * d6 corpses in it.

#### `fungus <nbr>`

Fungus income for the terrain when owned.

#### `gems <nbr>`

A bitmask value that determines the gem income of the location. See the Gem Income Bitmask table. Note that you can add multiple 1 income values together to create a higher income value of a certain type of gem. Maximum income for a single gem type is 7.

See also: `gems`

#### `gold <nbr>`

Gold income for the terrain when owned.

#### `hands <nbr>`

Hands of Glory income for the terrain when owned.

#### `herbs <nbr>`

Herb income for the terrain when owned.

#### `iron <nbr>`

Iron income for the terrain when owned.

#### `lifeforce <nbr>`

Sets amount of lifeforce that can be drained from the square * 10. A plain has 10 and a forest 30. Negative values means square drain lifeforce with this radius (Pillar of Power has a value of -1).

#### `name "name"`

Name of the terrain type.

#### `pop <nbr>`

A value indicating the size of humanlike population. Farm = 5, City = 50.

#### `sacr <nbr>`

Sacrifice income for the terrain when owned.

#### `spr "image.tga"`

Sets the image file for the terrain square.

#### `trade <nbr>`

Trade value of the terrain when owned.

#### `weed <nbr>`

Weed income for the terrain when owned.

### Terrain Modding > Clear Commands

#### `clearfort`

Clears the fort attributes of the selected terrain.

#### `clearspec`

Clears the special attributes of the selected terrain.

### Terrain Modding > Special Attributes

#### `anchored`

Dimensionally anchored location.

#### `barricade`

Wooden barricade gate

#### `batmap <batmap nbr>`

Associates the terrain with a certain battle map. See table Battle Maps . This is usually used for fortified locations, but villages also have a battle map.

See also: `batmaps`

#### `bonusrelics <value>`

Get this number of extra relics from this location. By default the amount of relics is one less than the amount of sacrifices earned.

#### `bramblegate`

Bramble gate

#### `burnable`

The terrain can be burned like forest.

#### `cave`

The terrain counts as a cave.

#### `citadel`

The terrain functions as a citadel when owned.

#### `cityname`

This terrain should start with a random city name.

#### `cloudgate`

Cloud gate

#### `deepspawn`

Hybrid fishermen can appear here.

#### `desert`

The terrain counts as a desert for the purposes of abilities like Desert Move.

#### `desertok`

Terrain will survive surroundings being turned into desert.

#### `destroyto <terrain nbr>`

Turns into this terrain when destroyed or burned up. Usually this command is not needed and it the terrain will be turned into something appropriate depending on its attributes.

#### `earthbarricade`

Earth barricade gate

#### `el`

Terrain starts as converted to the worship of El.

#### `enchantedgate`

The fort has an enchanted gate

#### `farsight`

The terrain gives increased vision range when there are units present there. Watchtowers and some citadels have this attribute.

#### `farvis`

Can be seen from far away.

#### `forest`

The terrain counts as forest for the purposes of abilities like Forest Stealth.

#### `forestcitadel`

Can be used as citadel by the Troll King.

#### `goldboost`

The terrain provides a global boost to gold income when owned.

#### `hardfly`

Difficult to fly here, costs 2 AP.

#### `harvest`

Structures with this command get double gold income during bumper harvest events. Farms have this attribute.

#### `hoburg`

All starting corpses here will be small size.

#### `invisible`

The sprite will not be drawn, instead the look of the terrain will be procedurally generated. Not a useful command for modding.

#### `invseason`

Seasons are reversed in this terrain.

#### `ironboost`

The terrain provides a global boost to iron income when owned.

#### `irongate`

The fort has an iron gate

#### `library1`

Library level +1.

#### `library2`

Library level +2.

#### `magicwalls`

Ethereal units cannot pass through walls at this fort

#### `melts`

A hint to the AI that the terrain melts after the winter. Frozen lakes and rivers have this attribute. Not a useful command for modding.

#### `mine`

The terrain counts as a mine.

#### `mistrare <chance>`

Will reduce the amount of mist produced. Rare is the chance in percent that mist will be produced.

#### `misty`

Mist emanates from here.

#### `mountain`

The terrain counts as a mountain for the purposes of abilities like Mountain Move.

#### `nevercold`

This square will never get cold.

#### `nodrown`

No one will drown in this terrain. Fishes can be on land and vice versa here. Used for frozen water tiles.

#### `nosight`

The terrain does not provide vision into adjacent squares when owned. Forests and swamps have this attribute.

#### `nosnowpen`

No movement penalty from snow.

#### `nostart`

Players cannot start in this type of terrain. Other squares can be overwritten by a start citadel from a player.

#### `nostdrec`

Standard class based recruitment lists are not available in this terrain. Instead, there are other units available for recruitment specific to the terrain.

#### `ownable`

The terrain can be claimed for ownership if it provides income the player can use.

#### `port`

Ships can enter this terrain.

#### `rare`

The terrain is a rare special terrain. It is sometimes deployed at a random place in Elysium by the random map generator.

#### `realport`

Ships can be recruited here.

#### `ritrebate <percent>`

All rituals cast on this location will be cheaper.

#### `seepast`

Far horizon (like sea).

#### `settlement`

Defines the terrain as a human settlement. Hamlets, villages, towns etc have this attribute.

#### `smoke`

Pixels with a certain pink color (245,0,255) will produce smoke. Pixels with color (235,0,255) will produce flames and smoke.

#### `snowok`

Income in this terrain is not affected by snow.

#### `spreadcold`

The terrain square spreads cold around it, turning nearby squares snowy.

#### `swamp`

The terrain counts as swamp for the purposes of abilities like Swamp Move.

#### `tempimmune`

The terrain will not be transformed into a wasteland when it gets too hot

#### `temple`

The terrain counts as a temple.

#### `town1`

One town point.

#### `town2`

Two town points.

#### `tradeboost`

The terrain provides a global boost to trade points when owned.

#### `ug`

This is an underground terrain.

#### `unique`

This terrain is unique and can only be placed once by the random map generator.

#### `useable`

There is a special power inherent to the terrain that can be activated by commander actions.

#### `visible`

Makes sure that the sprite is drawn as terrain and nothing else. Necessary to modify the look of procedurally drawn terrains like forests, mountains and villages.

#### `void`

The terrain is part of the void. It is possible to both walk, swim and sail here.

#### `voidret`

The terrain is connected to the Void. Use for Pyramids and other such structures.

#### `walls`

The location has walls in battle and is a siegable location.

#### `water`

The terrain is water and cannot be passed, unless it is frozen or the monsters moving through it are amphibian or aquatic.

#### `woodencitadel`

Can be used as citadel by the Senator

#### `woodengate`

The fort has a wooden gate

### Terrain Modding > Start Commands

#### `selectterr <terrain nbr>`

Select the terrain to be modified. Select a low number to alter an existing terrain or select a number between 500 - 999 to create a new terrain. Press ctrl-i in game on a terrain to see what number it has.

### Weapon Modding > Basic Commands

#### `aoe <nbr>`

Sets the area of effect for the weapon in squares. The default value is 0 (a single monster). A value of x will hit up to x monsters near the target. There are also many special values that can be used for other kind of areas. See Table Area of Effects (aoe) . Those that are written as e.g. 30xx must be written as a 4 digit number e.g. “aoe 3005” for a cone of 5 squares.

See also: `aoe`

#### `dmg <nbr>`

Sets the damage for the weapon. The default value is 0, which makes the weapon a natural weapon whose base damage is determined during monster modding. Note that damage types 12 and 13 require a bitmask value for their special effects. The special afflictions and benefit effects are listed in table Special Afflictions and table Special Benefits .

See also: `aff`, `ben`

#### `dmgtype <nbr>`

Sets the damage type for the weapon. Table Damage Types (dmgtype) contains the list of possible damage types. The default value is 3 (piercing damage).

See also: `dmgtype`

#### `init <nbr>`

Initiative value for the weapon, default is 2. Some common initiative values are these 1=spell, 2=fist/dagger/bow, 3=club/axe, 4=sword, 6=spear.

#### `range <nbr>`

The maximum range of the weapon. This should be 1 for melee weapons. A normal bow has range 5.

#### `trgrank <nbr>`

Sets the battlefield row where the weapon hits. See the Target Ranks (trgrank) table for the possible values. The default value is 1.

See also: `trgrank`

### Weapon Modding > Chained Weapons

#### `next`

If the target is wounded by the weapon, it will also be hit by the next weapon, i.e. the weapon defined next in the mod after this weapon. This command can only be used for new weapons, so you must have created one with the newweapon command.

#### `nextalways`

Like next, but will take effect even if no damage was inflicted on the target.

#### `nextalwayswep "weapon name" | <nbr>`

Like 'nextalways' but the additional strike will come from a named weapon that has already been created.

#### `nextdmg <dmg>`

Sets the damage of the chained weapon.

#### `nextwep "weapon name" | <nbr>`

Like 'next' but the additional strike will come from a named weapon that has already been created.

### Weapon Modding > Sound & Visuals

#### `blue`

set color of damage numbers

#### `flylook <look>`

The visual effect (see table Visual Effects (look) ) of the flying projectile, ranged weapons only. If flymode is 1 a fly sprite (see table Fly Sprites (flyspr) ) should be used instead of a look number.

See also: `look`, `flyspr`

#### `flymode <flymode nbr>`

Set this if a projectile should be visible for a ranged attack. See Fly modes (flymode) table. Those marked with an asterisk (*) behave like normal for aoe 1 effects, but with larger aoe they still only create one flying graphical effect. Fireball uses this effect to create a single flying fireball, but with a larger aoe explosion. If using a sprite (flymode 1) then the look value will be used to set the sprite used. See the table Fly Sprites (flyspr) for possible sprites to use.

See also: `flymode`, `flyspr`

#### `flysound <sound>`

The sound effect when the projectile starts flying, ranged weapons only. -1 = none.

#### `look <look>`

Sets the visual effect that occurs where the weapon strikes down, e.g. a fiery explosion for a fireball. See the Visual Effects (look) table. The default is no visual effect.

See also: `look`

#### `purple`

set color of damage numbers

#### `reloadsnd <sound>`

Sound when reloading, -1 = none.

#### `sndvol <dvol>`

dvol -50 = half volume, 100 = double volume.

#### `sound <sound>`

The sound effect when the weapon strikes down. See table Sound Effects (sound) .

See also: `sound`

#### `yellow`

set color of damage numbers

### Weapon Modding > Special Attributes

#### `affectanimal`

The weapon only affects animals.

#### `affecthuman`

The weapon only affects units with the res_convert attribute.

#### `affectmale`

This weapon will not affect females

#### `affectundead`

The weapon only affects undead.

#### `an`

The weapon ignores armor.

#### `arrow`

The effects of this weapon can be negated by the Air Shield attribute.

#### `clearwspec`

Clears all special attributes of the weapon.

#### `dispossess`

Victim becomes a dispossessed spirit

#### `drain`

Draining damage that will heal the attacker

#### `drown`

Water breathers are immune to this weapon.

#### `easymr`

Passing an easy magic resistance check negates the effects of this weapon.

#### `ethereal`

The weapon does not affect Ethereal beings

#### `flying`

Flying and Floating units are immune.

#### `flying2`

Flying units have 75% chance of evading this attack

#### `fullsweep`

The attack will hit all adjacent units. The primary target takes full damage and all subsequent targets take a cumulative -1 damage (so the second target takes full damage -1, the third target takes full damage -2 etc).

#### `ghoulify`

Humanoids killed by this weapon will become ghouls

#### `hardmorale`

A morale check vs 1d20 negates the effects of this weapon.

#### `hardmr`

Passing a hard magic resistance check negates the effects of this weapon.

#### `holykill`

The weapon causes double damage against undead & demons

#### `huge`

The weapon does not affect Huge beings.

#### `inanimate`

The weapon does not affect Lifeless beings.

#### `large`

The weapon does not affect monsters that are 2x2 tiles or larger in size on the battlefield.

#### `lob`

Use this command for arrows, sling stones and other weapons with an arcing trajectory.

#### `mind`

The weapon does not affect Mindless beings.

#### `morale`

A morale check vs 1d10 negates the effects of this weapon.

#### `mr`

Passing a normal magic resistance check negates the effects of this weapon.

#### `mundane`

Being Ethereal protects against this weapon. Ethereal units have a 75% chance to be unaffected by the weapon. Most weapons such as swords and spears are mundane.

#### `mutate`

A victim killed by this weapon becomes a monster of the type that immediately follows the killer in the monster list. For example, units killed by a Doppelganger become Doppelspawn, which is the next unit in order from Doppelganger.

#### `nostr`

The weapon is unaffected by damage bonuses from any source

#### `oneshot`

The weapon can only be used once per battle.

#### `onlyenemy`

This weapon will not affect friendly troops

#### `onlyfriend`

This weapon will only affect friendly troops

#### `poison`

Poison resistance helps against this attack even though the weapon is not poison.

#### `rangepen`

Damage penalty at long range. All normal range weapons like bows and slings have this.

#### `reanimate`

A victim killed by the weapon becomes a Soulless.

#### `reload1`

It takes 1 combat round to reload this weapon.

#### `reload2`

It takes 2 combat rounds to reload this weapon.

#### `reload3`

It takes 3 combat rounds to reload this weapon.

#### `replicate`

A victim killed by this weapon becomes the same type of monster as the killer.

#### `scatter`

A missile weapon with this attribute may deviate one square

#### `shieldneg`

The weapon ignores shields.

#### `soft`

Armor is doubled vs this weapon

#### `stone`

Stone beings are immune to the weapon.

#### `stonekill`

x2 dmg vs stone beings and stone walls

#### `strresist`

The effects of this weapon can be resisted by a successful strength check.

#### `sweep`

The weapon can continue to kill multiple targets.

#### `targterr`

Weapon can target terrain

#### `tree`

Tree/bushes/fungus are immune to this weapon

#### `undead`

The weapon does not affect Undead units.

#### `undkill`

The weapon causes double damage against undead only

#### `wallkill`

x5 dmg vs walls and boats

### Weapon Modding > Start Commands

#### `newweapon "weapon name"`

This command creates a new weapon.

#### `selectweapon "weapon name" | <nbr>`

Selects an existing weapon for modification. There may be several different weapons with the same name, in which case you should use the weapon number for selecting the desired weapon. You can see existing weapon numbers in game by pressing ctrl-i when inspecting a unit.

## Populum Usage Examples

### `absorbdead`

- L32032: `absorbdead 1`
- L32418: `absorbdead 1`
- L32424: `absorbdead 1`
- L33955: `absorbdead 1`
- L37555: `absorbdead 5`
- L37562: `absorbdead 10`
- L41819: `absorbdead 5`
- L41852: `absorbdead 2`

### `acutesenses`

- L692: `acutesenses`
- L21441: `acutesenses`
- L21466: `acutesenses`
- L21491: `acutesenses`
- L21516: `acutesenses`
- L21539: `acutesenses`
- L21568: `acutesenses`
- L21597: `acutesenses`

### `addcomrec`

- L76358: `addcomrec "Peddlar" 5 150 10 5`
- L76422: `addcomrec   "Slaver"                   25  100 0   0`
- L76423: `addcomrec   "Tribal Prince"                    5      0 0   0`
- L76424: `addcomrec   "Tribal Prince"                    100      0 0   0`
- L76426: `addcomrec   "Lion King"                    100      0 0   0`
- L76428: `addcomrec   "Slave Queen"                 100      0 0   0`
- L76432: `addcomrec   "Tribal King"                 100      0 0   0`
- L76434: `addcomrec   "Tribal Queen"                 100      0 0   0`

### `addeventvar`

- L57568: `addeventvar 455`  # adds 1 to pillage counter
- L57572: `addeventvar 375`  # adds 1 to migration pool
- L57605: `addeventvar 217`  # adds 1 to slavery counter
- L57609: `addeventvar 375`  # adds 1 to migration pool if the settlement reduces
- L57810: `addeventvar 731`  # adds 1 to experimentation counter
- L57814: `addeventvar 375`  # adds 1 to migration pool if the settlement reduces
- L57838: `addeventvar 731`  # adds 1 to experimentation counter
- L57842: `addeventvar 375`  # adds 1 to migration pool if the settlement reduces

### `addmercrec`

- L76359: `addmercrec  "Spearman"               60  5   100   0    0`
- L76360: `addmercrec  "Archer"                 60  5   100   0    0`
- L76361: `addmercrec  "Swordsman"                 40  5   100   0    5`
- L76362: `addmercrec  "Heavy Infantry"         40  5   50  200   10`
- L76363: `addmercrec  "Catapult"                        30  1   100   0   10`
- L76366: `addmercrec  "Trebuchet"                        20  1  150   0   20`
- L76369: `addmercrec  "Scout"                            10  1   15  10    0`  # once per offer; extra.
- L76370: `addmercrec  "Ballista"                         15  1  200   0   15`

### `addresources`

- L80598: `addresources -2 0 150`
- L80608: `addresources -2 0 125`
- L80618: `addresources -2 0 125`
- L80628: `addresources -2 0 75`
- L85875: `addresources -2 0 1500`  # Gold treasury
- L85876: `addresources -2 1  300`  # Iron treasury
- L85877: `addresources -2 14 100`  # random gems
- L85878: `addresources -2 5   10`  # Hands treasury

### `addstartcom`

- L76336: `addstartcom "Knight"`
- L76337: `addstartcom "Knight"`
- L76338: `addstartcom "Unexpected Hero"`
- L76339: `addstartcom "Heroine"`
- L76340: `addstartcom "Peddlar"`
- L76341: `addstartcom "Monk"`
- L76342: `addstartcom "Hedge Wizard"`
- L76343: `addstartcom "Cultist"`

### `addstartterr`

- L76534: `addstartterr 20`
- L76536: `addstartterr 5`
- L76581: `addstartterr 125`
- L76583: `addstartterr 125`
- L76665: `addstartterr 5`
- L76666: `addstartterr 154`
- L76717: `addstartterr 206`
- L76719: `addstartterr 5`

### `addstartunits`

- L76331: `addstartunits "Swordsman" 5`
- L76332: `addstartunits "Spearman"  10`
- L76333: `addstartunits "Archer" 10`
- L76334: `addstartunits "Cavalryman" 5`
- L76335: `addstartunits "Scout" 1`
- L76344: `addstartunits "Imp Familiar" 1`
- L76346: `addstartunits "Black Cat Familiar" 1`
- L76348: `addstartunits "Raven Familiar" 1`

### `addstring`

- L38300: `addstring "c*Young Phoenix"`
- L56961: `addstring "c*Chest - Sphere of Power"`  # Enchanter 4
- L56962: `addstring "c*Chest - Staff of Power"`  # Enchanter 4
- L56963: `addstring "c*Chest - Robe of Power"`  # Enchanter 4
- L56976: `addstring "c*Chest - Staff of the Magi"`  # Enchanter 3
- L56977: `addstring "c*Chest - Archmage's Spell Scroll"`  # Enchanter 3
- L56978: `addstring "c*Chest - Gem of True Seeing"`  # Enchanter 3
- L56979: `addstring "c*Chest - Helmet of Might"`  # Enchanter 3

### `addterr`

- L20789: `addterr 103`
- L20790: `addterr 106`
- L20791: `addterr 121`
- L20792: `addterr 157`
- L20797: `addterr 17`
- L20798: `addterr 79`
- L20799: `addterr 80`
- L20800: `addterr 81`

### `addunitrec`

- L76847: `addunitrec  "Soulless Soldier"                100  5    0   0    5`
- L76849: `addunitrec  "Armored Soulless"                100  5    0   0    5`
- L76851: `addunitrec  "Armored Longdead"                100  5    0   0    5`
- L76853: `addunitrec  "Bane Fire Archer"                100  5    0   0    0`
- L76856: `addunitrec  "Bane-Bones"                      100  5    0   0    5`
- L77117: `addunitrec  "Tengu Warrior"                    15  3   150   0   15`  # once per offer.
- L77537: `addunitrec  "Ember Warrior"                    75  2  0   0    0`
- L77540: `addunitrec  "Flame Spirit"                     25  1  0   0    0`  # once per offer.

### `addvar`

- L86641: `addvar 375 1`  # Add 1 to migration/ population pool
- L86651: `addvar 375 1`  # Add 1 to migration/ population pool
- L86661: `addvar 375 1`  # Add 1 to migration/ population pool
- L86672: `addvar 375 1`  # Add 1 to migration/ population pool

### `affectanimal`

- L7546: `affectanimal`
- L14068: `affectanimal`
- L14094: `affectanimal`
- L14120: `affectanimal`
- L18819: `affectanimal`  # Only affects animals

### `affecthuman`

- L4158: `affecthuman`
- L4413: `affecthuman`
- L8196: `affecthuman`
- L9077: `affecthuman`
- L9103: `affecthuman`
- L9129: `affecthuman`
- L9285: `affecthuman`
- L19131: `affecthuman`  # Only affects humans

### `affectmale`

- L4415: `affectmale`
- L4432: `affectmale`
- L20349: `affectmale`

### `affectundead`

- L7843: `affectundead`
- L20271: `affectundead`
- L20286: `affectundead`

### `affres`

- L694: `affres 100`
- L25202: `affres 100`
- L25204: `affres 100`
- L25206: `affres 100`
- L25244: `affres 100`
- L25355: `affres 100`
- L25357: `affres 100`
- L25359: `affres 100`

### `aggressive`

- L30105: `aggressive`
- L30113: `aggressive`
- L30246: `aggressive`
- L30467: `aggressive`
- L30474: `aggressive`
- L30551: `aggressive`
- L31003: `aggressive`
- L31007: `aggressive`

### `aialways`

- L57523: `aialways 999`
- L58093: `aialways 999`
- L59113: `aialways 50`
- L59150: `aialways 90`
- L59184: `aialways 90`
- L59668: `aialways 90`
- L59752: `aialways 90`
- L63630: `aialways             100`  # AI will always try to cast this ritual if it currently can, but it will not make long term plans to do so.

### `aiapprspam`

- L57625: `aiapprspam 50`
- L57657: `aiapprspam 50`
- L57800: `aiapprspam 5`
- L57829: `aiapprspam 5`
- L58399: `aiapprspam 5`
- L58429: `aiapprspam 5`
- L58462: `aiapprspam 5`
- L58493: `aiapprspam 5`

### `aiclass`

- L77837: `aiclass 0`
- L77892: `aiclass 0`
- L78109: `aiclass -1`

### `aigoldrally`

- L30577: `aigoldrally 1`
- L30590: `aigoldrally 1`
- L30936: `aigoldrally      1`
- L48832: `aigoldrally 1`

### `aihold`

- L31438: `aihold 1`
- L41447: `aihold 1`
- L41510: `aihold 1`
- L41574: `aihold 1`
- L42884: `aihold 1`
- L52437: `aihold 1`
- L52519: `aihold 1`

### `aimaxcast`

- L58857: `aimaxcast 15`
- L73491: `aimaxcast 10`

### `ainofollower`

- L22262: `ainofollower     1`
- L30578: `ainofollower`
- L30591: `ainofollower`
- L31110: `ainofollower`
- L48831: `ainofollower`
- L55537: `ainofollower`
- L55556: `ainofollower`
- L55574: `ainofollower`

### `ainosimul`

- L57548: `ainosimul`
- L57583: `ainosimul`
- L58920: `ainosimul`
- L58948: `ainosimul`
- L73249: `ainosimul`

### `ainotclose1`

- L75555: `ainotclose1 5`

### `ainotclose3`

- L57881: `ainotclose3 197`
- L58856: `ainotclose3 28`
- L58873: `ainotclose3 26`
- L59985: `ainotclose3 126`
- L60540: `ainotclose3 197`
- L65478: `ainotclose3 154`
- L65606: `ainotclose3 13`
- L65682: `ainotclose3 92`

### `ainotnearhome`

- L57547: `ainotnearhome 20`
- L57582: `ainotnearhome 15`
- L57801: `ainotnearhome 15`
- L57830: `ainotnearhome 15`
- L57880: `ainotnearhome 10`
- L58094: `ainotnearhome 15`
- L58797: `ainotnearhome 15`
- L58872: `ainotnearhome 15`

### `aipowcom2`

- L46115: `aipowcom2 -1`
- L46136: `aipowcom2 -1`

### `airare`

- L56944: `airare -1`
- L56959: `airare -1`
- L56972: `airare -1`
- L56994: `airare -1`
- L57059: `airare -1`
- L57080: `airare -1`
- L57100: `airare -1`
- L57119: `airare -1`

### `airestrig`

- L75344: `airestrig 1000`
- L75380: `airestrig 2000`

### `airshield`

- L26672: `airshield 25`
- L26674: `airshield 25`
- L26676: `airshield 25`
- L26678: `airshield 50`
- L26680: `airshield 25`
- L26682: `airshield 25`
- L26684: `airshield 25`
- L26686: `airshield 25`

### `aiweakonly`

- L58322: `aiweakonly 500`
- L59112: `aiweakonly 500`
- L59149: `aiweakonly 500`
- L59183: `aiweakonly 500`
- L59458: `aiweakonly 1000`
- L59481: `aiweakonly 500`  # 50 spearmen equiv
- L59667: `aiweakonly 500`
- L59751: `aiweakonly 500`

### `allitemslots`

- L21543: `allitemslots`
- L21664: `allitemslots`
- L21696: `allitemslots`
- L21728: `allitemslots`
- L21846: `allitemslots`
- L22232: `allitemslots`
- L24593: `allitemslots`
- L24960: `allitemslots`

### `allrit`

- L32022: `allrit 39`
- L42601: `allrit 18`
- L42644: `allrit 19`
- L42688: `allrit -1`
- L42730: `allrit -1`
- L42772: `allrit -1`
- L42817: `allrit -1`
- L43868: `allrit          -1`  # Knows all rituals of all powers (practiced by it)

### `alterloc`

- L57632: `alterloc 12`  # Mountain
- L57634: `alterloc              105`  # Coal mine
- L57636: `alterloc              33`  # Gold Stream
- L57666: `alterloc 105`  # Coal Mine
- L57668: `alterloc              14`  # Iron mine
- L57671: `alterloc              15`  # Silver Mine
- L57674: `alterloc              34`  # Gold Mine
- L57882: `alterloc              197`  # Change target location to f-circle

### `alterterrain`

- L80578: `alterterrain 511`  # Cloud castle in clouds
- L80588: `alterterrain 4`  # Ancient forest
- L80674: `alterterrain 2`
- L80683: `alterterrain 115`
- L86505: `alterterrain 4`  # Ancient forest
- L86555: `alterterrain 2`
- L86564: `alterterrain 115`

### `an`

- L3575: `an`  # Armor negating
- L3604: `an`
- L3613: `an`
- L3622: `an`
- L3647: `an`  # Armor negating
- L3663: `an`  # Armor negating
- L3724: `an`
- L3734: `an`

### `ancforest1`

- L56662: `ancforest1`  # Loves ancient forests (if an independent or stupid commander, will not leave its loved terrains).

### `anchored`

- L85314: `anchored`

### `animal`

- L22209: `animal`
- L24674: `animal`
- L30304: `animal`
- L38236: `animal`
- L38241: `animal`
- L38245: `animal`
- L38248: `animal`
- L38252: `animal`

### `aoe`

- L3511: `aoe 99`
- L3519: `aoe 99`
- L3527: `aoe 2002`
- L3535: `aoe 2002`
- L3543: `aoe 2002`
- L3553: `aoe     9999`  # All squares
- L3559: `aoe      999`  # All enemies
- L3632: `aoe     7100`  # Far crack 100

### `apcost`

- L56943: `apcost -1`
- L57176: `apcost 3`
- L57478: `apcost 3`
- L57493: `apcost 2`
- L57542: `apcost 1`
- L57581: `apcost 1`
- L57620: `apcost 3`
- L57654: `apcost 3`  # Actual AP cost: cost+1

### `armor`

- L696: `armor 1`
- L21432: `armor            1`
- L21457: `armor            1`
- L21482: `armor            1`
- L21507: `armor            1`
- L21531: `armor          0`
- L21558: `armor          0`
- L21587: `armor          0`

### `armytrainer`

- L33073: `armytrainer 3`

### `arrow`

- L4118: `arrow`  # Can be deflected by air shield
- L4226: `arrow`  # Can be deflected by air shield
- L4263: `arrow`
- L4607: `arrow`  # Can be deflected by air shield
- L4623: `arrow`  # Can be deflected by air shield
- L4724: `arrow`
- L4758: `arrow`
- L4993: `arrow`

### `assassinweapon`

- L21537: `assassinweapon     1 729`  # Dream Seduction (value 1: charm)
- L28726: `assassinweapon     1 405`
- L29638: `assassinweapon    10 659`
- L41306: `assassinweapon 9999 "Kill Self"`
- L41326: `assassinweapon 9999 "Kill Self"`
- L41343: `assassinweapon 1 "Kill Self"`
- L44150: `assassinweapon     2 182`
- L47905: `assassinweapon 20 "Charm Cheat"`

### `awe`

- L21550: `awe              1`
- L33476: `awe 2`
- L37218: `awe 2`
- L37225: `awe 1`
- L37247: `awe 1`
- L37251: `awe 2`
- L37260: `awe 1`
- L37269: `awe 2`

### `badsight`

- L40221: `badsight`
- L40240: `badsight`
- L40260: `badsight`
- L49418: `badsight`
- L49565: `badsight`
- L49614: `badsight`
- L49639: `badsight`
- L49665: `badsight`

### `banishsurv`

- L21545: `banishsurv`  # Not killed when banished. Goes to Hades/Inferno/home
- L21574: `banishsurv`  # Not killed when banished. Goes to Hades/Inferno/home
- L21603: `banishsurv`  # Not killed when banished. Goes to Hades/Inferno/home
- L21634: `banishsurv`  # Not killed when banished. Goes to Hades/Inferno/home
- L21665: `banishsurv`  # Not killed when banished. Goes to Hades/Inferno/home
- L21697: `banishsurv`  # Not killed when banished. Goes to Hades/Inferno/home
- L21729: `banishsurv`  # Not killed when banished. Goes to Hades/Inferno/home
- L21756: `banishsurv`  # Not killed when banished. Goes to Hades/Inferno/home

### `batmap`

- L79152: `batmap 33`
- L79169: `batmap 6`
- L79188: `batmap 35`
- L79205: `batmap 26`
- L79220: `batmap 21`
- L79233: `batmap 12`
- L79288: `batmap 39`
- L79391: `batmap           28`  # Battle map: port.

### `battlefast`

- L22090: `battlefast`
- L22183: `battlefast`
- L22524: `battlefast`
- L22549: `battlefast`
- L22572: `battlefast`
- L22596: `battlefast`
- L22645: `battlefast`
- L22669: `battlefast`

### `battleslow`

- L41919: `battleslow`
- L42180: `battleslow`
- L42232: `battleslow`
- L45015: `battleslow`
- L46467: `battleslow`

### `battleslow2`

- L48064: `battleslow2`  # changed to the slower version

### `benrestrict`

- L61870: `benrestrict 4096`  # No Regeneration

### `bentarg`

- L58032: `bentarg               64`  # Gives the target this benefit: magic resistance +2
- L61875: `bentarg 4096`
- L71230: `bentarg 32768`
- L72779: `bentarg 16777216`  # Non-magic invul

### `bentargall`

- L61637: `bentargall  16`  # Gives the target this benefit: poison res
- L61988: `bentargall                 4`  # Gives the target this benefit: fire res

### `berserker`

- L28024: `berserker`
- L30089: `berserker`
- L30106: `berserker`
- L31921: `berserker`
- L31946: `berserker`
- L33046: `berserker`
- L33049: `berserker`
- L33058: `berserker`

### `blue`

- L5262: `blue`
- L8844: `blue`
- L12836: `blue`

### `bluntres`

- L21444: `bluntres`  # Blunt resistance
- L21469: `bluntres`  # Blunt resistance
- L21494: `bluntres`  # Blunt resistance
- L21519: `bluntres`  # Blunt resistance
- L22210: `bluntres`  # Blunt resistance
- L22258: `bluntres`  # Blunt resistance
- L24240: `bluntres`  # Blunt resistance
- L24389: `bluntres`  # Blunt resistance

### `bonusrelics`

- L79530: `bonusrelics       1`  # Get 1 extra relics from this location. (Total 3 relics with temple and hands 2)
- L85315: `bonusrelics 2`
- L85794: `bonusrelics -1`

### `burnforest`

- L22070: `burnforest       3`
- L22132: `burnforest       3`
- L22161: `burnforest       3`
- L42589: `burnforest 20`
- L48162: `burnforest 1`
- L48331: `burnforest 5`
- L48355: `burnforest 5`
- L48591: `burnforest 25`

### `castertarg`

- L57502: `castertarg`
- L57584: `castertarg`
- L57630: `castertarg`
- L57780: `castertarg`
- L58016: `castertarg`
- L58136: `castertarg`
- L58675: `castertarg`
- L58708: `castertarg`

### `cave`

- L79352: `cave`  # Deep chasm and crystalline formations.
- L79670: `cave`  # The terrain counts as a cave.
- L79801: `cave`  # The terrain counts as a cave.

### `centercaster`

- L69103: `centercaster`
- L73378: `centercaster`

### `centerloc`

- L58718: `centerloc`
- L59222: `centerloc`
- L59340: `centerloc`
- L59384: `centerloc`
- L60858: `centerloc`
- L61072: `centerloc`
- L61090: `centerloc`
- L62812: `centerloc`

### `changetemp`

- L30660: `changetemp 3`
- L30665: `changetemp 5`
- L33607: `changetemp -1`
- L37465: `changetemp -3`
- L37468: `changetemp -5`
- L37471: `changetemp 15`
- L44247: `changetemp     -15`
- L44282: `changetemp     -20`

### `charmres`

- L21570: `charmres`  # Charm immunity
- L21599: `charmres`  # Charm immunity
- L21630: `charmres`  # Charm immunity
- L21659: `charmres`  # Charm immunity
- L21690: `charmres`  # Charm immunity
- L21722: `charmres`  # Charm immunity
- L21752: `charmres`  # Charm immunity
- L21784: `charmres`  # Charm immunity

### `choosefxtarg`

- L58031: `choosefxtarg          90`  # Player chooses a target, which must have this feature: troll.
- L74264: `choosefxtarg 0`

### `chooseloc`

- L61385: `chooseloc              5`  # Player chooses the target location, which may deviate to a location with a horror marked unit.
- L61405: `chooseloc              5`  # Player chooses the target location, which may deviate to a location with a horror marked unit.
- L62436: `chooseloc              2`  # Player chooses the target location, which may deviate to a location with many corpses.
- L65088: `chooseloc 1`
- L69105: `chooseloc 1`
- L70875: `chooseloc              1`  # Player chooses the target location, which may deviate to a location with a horror marked unit.
- L70886: `chooseloc              1`  # Player chooses the target location, which may deviate to a location with a horror marked unit.
- L70897: `chooseloc              1`  # Player chooses the target location, which may deviate to a location with a horror marked unit.

### `chooseterrloc`

- L57896: `chooseterrloc        -10`  # Player chooses the target location, which must have this terrain: Ancient Forest.
- L60599: `chooseterrloc        -11`  # Player chooses the target location, which must have this terrain: Ancient Forest.
- L60614: `chooseterrloc         -6`  # Player chooses the target location, which must have this terrain:Forest / jungle / ancient forest.
- L60948: `chooseterrloc        -3`  # Required terrain: Magic Libs
- L60960: `chooseterrloc -1`
- L60987: `chooseterrloc        -3`  # Required terrain: Magic Libs
- L60999: `chooseterrloc -1`
- L61086: `chooseterrloc        -1013`  # Required terrain: settlements

### `citadel`

- L79148: `citadel`
- L79166: `citadel`
- L79181: `citadel`
- L79196: `citadel`
- L79212: `citadel`
- L79255: `citadel`  # The terrain functions as a citadel when owned.
- L79272: `citadel`  # The terrain functions as a citadel when owned.
- L79290: `citadel`

### `classabdescr`

- L78757: `classabdescr "The Cloud Lord starts with a citadel in the ‘Sky realm’ near a mountain top.^The Airya armies can fly over difficult terrains and between clouds.^Airya elites can be recruited for an additional cost in gems, but reduced gold cost.^^Eagle Kings, Cloud Lords and Cloud Casters collect gems.^Air Gems can be used for magic rituals. Other gems can be converted to air gems with an alchemy ritual, or used to recruit elite units."`
- L78822: `classabdescr "Kobolds come in several colors, each with their own strengths, but all are weak.^^Kings and Prophets enable the recruitment of Dragon Spawn.^^Great Mines and Kobold Strongholds produce free kobolds corresponding to the gems produced in the mine.^^The Kobold King, shamans and sorcerers collect gems.^^Gems can be used for magic rituals to create strongholds, traps, or summon guardian dragons.^^Cannot recruit humans in castles or other special locations."`
- L78874: `classabdescr "Small Markatas can be recruited in great numbers, forming the backbone of the workforce and light skirmishers. Bandars are large, powerful apes, serving as elite warriors and leaders. Bandarajas can recruit heavily armed Bandars. Atavi villages, when allied or conquered, will provide Markatas and Atavi tribesmen over time. White One Yogis, Gurus, and Rishis are powerful casters who collect gems. Gems are crucial for invoking ancient jungle spirits and performing potent nature rituals. Can build unique jungle-themed fortifications and shrines."`
- L78946: `classabdescr "Markatas and other lesser monkey-folk serve as numerous but expendable troops. Bandars, corrupted by demonic influence, become fearsome half-demon warriors. Raksharajas and their inner circle (Rakshasa Generals, Raktapatas, Kala-Mukhas) are powerful casters collecting sacrifices. Sacrifices fuel potent rituals: summoning demonic Rakshasas, reanimating the dead as loyal servants, and casting grand illusions to deceive and demoralize foes. Can use Maya to shroud their armies and settlements, making them appear as simple monkey tribes or uninhabited jungle. Access to unique Rakshasa units with illusionary and fear-inducing abilities."`
- L79059: `classabdescr "Regular human troops of good quality.^Guilds can be built in places of trade.^Different Guilds improve different economic aspects.^Different Guilds can give access to elite or exotic troops as well as mages and other special commanders.^Some guilds generate free units, some of which move around independently.^Mercenary Guilds increases the number of mercenary offers."`
- L80430: `classabdescr "Starts in a very well fortified castle.^25% increase to gold income.^25% increase to iron income.^Conscription yields soldiers from settlements and ancient forests once every year.^The Baron and High Lords can raise levies (immobile defenders) in villages and towns."`
- L80434: `classabdescr "Starts in a very well fortified dark citadel.^Necromancers can sense the amount of dead where they are.^Necromancers can raise the dead for the price of some sanity.^Necromancers collect Hands of Glory from large villages and towns.^Necromancers can use Hands of Glory to perform rituals to summon undead beings and enter the underworld."`
- L80438: `classabdescr "Starts in a very well fortified citadel.^Demonologists collect sacrifices from hamlets, villages and towns.^Demonologists can use sacrifices to summon and bind demons or open infernal gates."`

### `classcitterr`

- L76389: `classcitterr -1005`  # "Temple city, tribal and tent villages"
- L76469: `classcitterr -1005`  # "Temple city, tribal and tent villages"
- L76557: `classcitterr -1001`  # Towns and ports
- L76597: `classcitterr -1014`
- L76670: `classcitterr -32`
- L76712: `classcitterr -108`  # castles suitable for the Baron
- L76805: `classcitterr -78`  # Hades plane
- L76944: `classcitterr -8`  # Villages and smaller

### `classcost`

- L30949: `classcost -15`
- L30978: `classcost -30`
- L31342: `classcost 1`
- L31350: `classcost 1`
- L31358: `classcost 1`
- L31366: `classcost 1`
- L31370: `classcost 1`
- L31522: `classcost 100`

### `classdescr`

- L76380: `classdescr "NPC boss faction that builds slave armies with low to zero magic.^^In one hundred years a god will be automatically released unless you destroy the altar.^^Only one Blood Tide may exist, add separate slave king NPCs to the Blood Tide team to increase the power of this faction. Clustering tends to weaken AI teams, but depends on map size and layout.^^For largest size maps set difficulty to Emperor and decrease by one difficulty for each map size reduction."`
- L76461: `classdescr "An NPC nuisance faction that builds slave armies with low to zero magic. Add this faction to the Blood Tide's team to increase its influence. By itself the Slave King is weak. Clustering also weakens the team in some circumstances.^^For largest size maps set difficulty to King and decrease by one difficulty for each map size reduction."`
- L76530: `classdescr "Adding Independent Town NPCs allows the player to quickly add towns and population to a map. Each Independent town starts with a guard tower and farm.^^For largest size maps set difficulty to Knight regardless of map size."`
- L76577: `classdescr "A government with corrupt leaders that use their power to exploit the people and natural resources of their own territory in order to extend their personal wealth and political power.^^Bandit King is an NPC nuisance faction that can add flavor to an automatically generated map.^^For largest size maps set difficulty to King and decrease by one difficulty for each map size reduction."`
- L77852: `classdescr "A Technocratic Mageocracy where decision-makers are selected on the basis of magical knowledge. A variant start focusing on magic users but with very weak non-mage recruitment options.^^Abilities:^Starts with a level 2 library and Old Wizard who is capable of becoming an Archmage.^Access to many resources but weak standard troop recruitment."`
- L77922: `classdescr "The Goblin Emperor is an NPC nuisance faction adding flavor to a generated map. The Goblin Emperor on the Populum custom map is balanced for an Emperor difficulty with a Republic (Senator) start. The Goblin Emperor is most powerful early game being able to raise large armies quickly but falls off when facing powerful magical casters.^^For largest size maps set difficulty to Emperor and decrease by one difficulty for each map size reduction."`
- L78097: `classdescr "Spawn as a spectator soul with no ability to interact with game except as a passive watcher."`
- L78707: `classdescr "Government by those who seek chiefly status and personal gain at the expense of the governed.^^The Scourge Lord is the undisputed ruler of the land, as it is he who determines which people should be allowed to live and which should be drained of their life to fuel the Scourge Lord's power.  The Scourge Lords is able to grant great power to his foremost servants.  These servants are called Heralds and they enforce the Scourge Lord's laws and expand his influence by conquering neighboring areas.^^For lesser spells the Scourge Lord and his Herald can drain life force from vegetation or living beings in the immediate surroundings.  But for powerful rituals, much more life force is needed, and for this purpose great pillars or pyramids are built that can extract life force from the surrounding lands.  Anything in the vicinity of such a site of power will soon be turned into barren wastelands as the very life is drained from the land.  Some living beings from such area will be turned into Ghouls and continue to serve the Scourge Lord, but most will simply die as their life force is stolen.^^These rituals of the Scourge Lord are very powerful and can be used to summon and control beasts, teleport entire armies or to further enhance the might of the Scourge Lord and his Heralds. The Scourge Lord will not share power and there can only be one master. Only if the Lord becomes a King will he allow his Heralds to advance in power and become Scourge Lords."`

### `classforestcit`

- L77637: `classforestcit      1`  # Can use all kinds of ancient forests and sacred groves as citadels.
- L77926: `classforestcit      1`  # Can use all kinds of ancient forests and sacred groves as citadels.

### `clearmove`

- L25514: `clearmove`
- L30320: `clearmove`
- L30355: `clearmove`
- L30390: `clearmove`
- L30836: `clearmove`
- L31445: `clearmove`
- L31562: `clearmove`
- L31650: `clearmove`

### `clearrec`

- L76325: `clearrec`
- L76637: `clearrec`
- L76705: `clearrec`
- L76801: `clearrec`
- L76882: `clearrec`
- L76938: `clearrec`
- L77015: `clearrec`
- L77076: `clearrec`

### `clearspec`

- L21427: `clearspec`
- L21453: `clearspec`
- L21478: `clearspec`
- L21503: `clearspec`
- L21527: `clearspec`
- L21554: `clearspec`
- L21583: `clearspec`
- L21614: `clearspec`

### `clearstartterr`

- L76327: `clearstartterr`
- L76384: `clearstartterr`
- L76464: `clearstartterr`
- L76635: `clearstartterr`
- L76707: `clearstartterr`
- L76803: `clearstartterr`
- L76884: `clearstartterr`
- L76940: `clearstartterr`

### `clearstartunits`

- L76326: `clearstartunits`
- L76383: `clearstartunits`
- L76463: `clearstartunits`
- L76636: `clearstartunits`
- L76706: `clearstartunits`
- L76802: `clearstartunits`
- L76883: `clearstartunits`
- L76939: `clearstartunits`

### `clearweapons`

- L2302: `clearweapons`
- L2309: `clearweapons`
- L21426: `clearweapons`
- L21452: `clearweapons`
- L21477: `clearweapons`
- L21502: `clearweapons`
- L21526: `clearweapons`
- L21553: `clearweapons`

### `clearwspec`

- L18968: `clearwspec`
- L19212: `clearwspec`

### `closewin`

- L57900: `closewin`  # Closes cast ritual window.
- L58719: `closewin`
- L58846: `closewin`  # Closes cast ritual window.
- L59223: `closewin`
- L59341: `closewin`
- L59385: `closewin`
- L60377: `closewin`  # Closes cast ritual window.
- L60603: `closewin`  # Closes cast ritual window.

### `cloudgate`

- L79219: `cloudgate`
- L84416: `cloudgate`

### `coastal`

- L49984: `coastal`
- L56534: `coastal`  # Always stays within 1 square (including diagonals) of both land and water.

### `coldaura`

- L22134: `coldaura         5`
- L44380: `coldaura         2`

### `coldblood`

- L38133: `coldblood`
- L39664: `coldblood`  # Gets -1 to its strength in snow
- L39679: `coldblood`  # Gets -1 to its strength in snow
- L39701: `coldblood`  # Gets -1 to its strength in snow
- L39715: `coldblood`  # Gets -1 to its strength in snow
- L42378: `coldblood`  # Gets -1 to its strength in snow
- L42489: `coldblood`  # Gets -1 to its strength in snow
- L42558: `coldblood`

### `coldheal`

- L33545: `coldheal  1`
- L33600: `coldheal  2`
- L47884: `coldheal 2`

### `coldres`

- L21565: `coldres        100`  # Cold immunity
- L21594: `coldres        100`  # Cold immunity
- L21625: `coldres        100`  # Cold immunity
- L21654: `coldres        100`  # Cold immunity
- L21685: `coldres        100`  # Cold immunity
- L21717: `coldres        100`  # Cold immunity
- L21747: `coldres        100`  # Cold immunity
- L21779: `coldres        100`  # Cold immunity

### `copyspr`

- L24949: `copyspr " Priest King"`
- L24967: `copyspr " High Priest of the Sun"`
- L24985: `copyspr " Tribal King"`
- L28781: `copyspr   "Fire Dragon"`
- L28797: `copyspr   "Fire Dragon Hatchling"`
- L30069: `copyspr " Centaur"`
- L30112: `copyspr " Minotaur"`
- L30267: `copyspr " Purple Worm"`

### `copystats`

- L28780: `copystats "Fire Dragon"`
- L28796: `copystats "Fire Dragon Hatchling"`
- L30068: `copystats " Centaur"`
- L30111: `copystats " Minotaur"`
- L30317: `copystats "Renata"`
- L30352: `copystats "Renata"`
- L30387: `copystats "Renata"`
- L30472: `copystats " Troll"`

### `cost`

- L56956: `cost 0 1500`
- L56957: `cost 15 150`
- L56969: `cost 0  500`
- L56970: `cost 15  50`
- L56991: `cost 0  250`
- L56992: `cost 15  25`
- L57056: `cost 0  500`
- L57057: `cost 5  100`

### `createcit`

- L77189: `createcit         121`  # Other-planar home citadel: Pale One Lair.
- L78773: `createcit         265`  # Other-planar home citadel: Cloud Palace.

### `ctrlchance`

- L21547: `ctrlchance      60`  # Overrides control chance in any summoning ritual
- L24804: `ctrlchance     100`  # Overrides control chance in any summoning ritual
- L24880: `ctrlchance     100`  # Overrides control chance in any summoning ritual
- L30443: `ctrlchance 100`
- L31207: `ctrlchance 1000`
- L31218: `ctrlchance 1000`
- L31238: `ctrlchance 1000`
- L31249: `ctrlchance 1000`

### `cureoneaff`

- L72227: `cureoneaff`

### `dead`

- L79253: `dead              4`  # The location starts with 4 * d6 corpses in it.
- L79270: `dead              4`  # The location starts with 4 * d6 corpses in it.
- L79285: `dead 5`
- L79312: `dead              1`  # Some history or minor casualties.
- L79487: `dead             15`  # The location starts with 15 * d6 corpses in it. (High number for cemetery)
- L79784: `dead              2`  # The location starts with 2 * d6 corpses in it.
- L79859: `dead              1`  # The location starts with 1 * d6 corpses in it.
- L80015: `dead              1`  # The location starts with 1 * d6 corpses in it.

### `deadforest1`

- L42226: `deadforest1`

### `deadforest2`

- L42183: `deadforest2`

### `defctrl`

- L57551: `defctrl              -100`  # % default control chance for summonings. Can be overridden by monster's own ctrlchance.
- L57802: `defctrl               75`  # % default control chance for summonings. Can be overridden by monster's own ctrlchance.
- L57826: `defctrl               80`  # % default control chance for summonings. Can be overridden by monster's own ctrlchance.
- L58143: `defctrl 100`
- L58324: `defctrl              100`  # % default control chance for summonings. Can be overridden by monster's own ctrlchance.
- L58799: `defctrl             -100`  # % default control chance for summonings. Can be overridden by monster's own ctrlchance.
- L58928: `defctrl              -100`  # % default control chance for summonings. Can be overridden by monster's own ctrlchance.
- L58956: `defctrl              -100`  # % default control chance for summonings. Can be overridden by monster's own ctrlchance.

### `demonic`

- L45: `demonic`

### `deployoutside`

- L33962: `deployoutside 1`
- L33964: `deployoutside 1`
- L33966: `deployoutside 1`
- L33968: `deployoutside 1`
- L33970: `deployoutside 1`
- L33972: `deployoutside 1`
- L33974: `deployoutside 1`
- L33976: `deployoutside 1`

### `descr`

- L97: `descr "A militia is generally an army or some other fighting organization of non-professional soldiers, citizens of a country, or subjects of a state, who may perform military service during a time of need, as opposed to a professional force of regular, full-time military personnel.^^Militia must be at a human settlement or they will take attrition damage each month."`
- L30036: `descr "This Centaur Offspring will grow to adolescence in less than a year."`
- L30051: `descr "This Young Centaur will grow to military age about two years."`
- L30067: `descr "Centaurs are half-humanoid and half-equine humaniods."`
- L30076: `descr "This Minotaur Offspring will grow to adolescence in less than a year."`
- L30093: `descr "This Young Minotaur will grow to military age about three years."`
- L30110: `descr "It is disputed whether the Minotaur is a beast or a humanoid, because it has been seen associating with both Brigands and Deer.  That it can wield and use weapons effectively speaks for humanoid, but the fact that the Minotaur cannot speak indicates it is a beast.  Until more research has been done, it is safest to assume that the Minotaurs are beasts and stay away or kill them when possible."`
- L30266: `descr "The Purple Worms are truly gigantic in size and they eat the only thing that is available in the quantities needed to sustain such a huge thing, earth.  The worms are seldom seen despite their size, because they spend all their time deep below the surface of Elysium.  However those visiting the deep earth cannot miss the work of the worms as they walk in the vast empty caves left in the wake of the enormous worms.  Modern research proves that it was the Purple Worms that ate the parts that later became Inferno.  The devils settling there forced the worms to move closer to Elysium, where they currently reside and are likely to do so until something very powerful wants their newly created caverns for itself."`

### `description`

- L2: `description "Populum (latin for People) mod's goal is to link all the classes together in a thematic story-like fashion based loosely on systems of government connecting to social, political, and economic attributes. Populum increases the depth of the economy management and expands the early and late game of the classes by introducing new options.^^Some classes are meant for the AI only and are tagged with an '(NPC)' at the end of the class name. I would not recommend using these NPC classes because they are designed to be played by the AI with significant bonuses. These classes include: Goblin Emperor, Slave King, Independent Town, Bandit King, and the boss class called 'Blood Tide' which you may only have one due to the unique boss that comes with it. These classes were designed with the intent to be difficult early game enemies and mere nuisance to late-game players. The NPC classes are useful to quickly add flavor to a generated map. The NPC classes have their recommended difficulty built into the class name and are designed for the largest map size (enormous or custom larger). You may want to decrease an NPCs difficulty by one for 1-2 map size class reductions. For example the Goblin Emperor on enormous+ is played on Emperor difficulty; reduce to King for a Huge map, Duke for Large, Marquis for Medium, and anything smaller set to Count.^^Content Warning: This mod contains content (textual and game mechanics, not imagery) that may make some people uncomfortable including: Violence, Kidnapping and abduction, Enslavement, Death or dying, Pregnancy/Childbirth, Mental illness, Sexual Assault, Abuse, Animal cruelty or animal death, Self-harm and suicide, Eating disorders, Racism, Sexism and misogyny, and Classism."`

### `desert1`

- L35489: `desert1`

### `desert2`

- L35466: `desert2`
- L35470: `desert2`

### `desert3`

- L56535: `desert3`  # Hates deserts.

### `desertok`

- L79401: `desertok`  # Beaches can appear in southern/desert regions.
- L79750: `desertok`  # Fits desert environments.

### `destroyterr`

- L58925: `destroyterr`
- L58953: `destroyterr`
- L59012: `destroyterr 100`
- L62654: `destroyterr 33`  # % chance of destroying the terrain.
- L64204: `destroyterr 15`
- L66320: `destroyterr 100`
- L66720: `destroyterr 33`
- L66973: `destroyterr 100`

### `destroyto`

- L79261: `destroyto 12`
- L79276: `destroyto 0`

### `digest`

- L30280: `digest           2`

### `diseasecloud`

- L43874: `diseasecloud 8`
- L47840: `diseasecloud 2`

### `diseaseres`

- L1788: `diseaseres`
- L21540: `diseaseres`  # Disease immunity
- L21572: `diseaseres`  # Disease immunity
- L21601: `diseaseres`  # Disease immunity
- L21632: `diseaseres`  # Disease immunity
- L21661: `diseaseres`  # Disease immunity
- L21692: `diseaseres`  # Disease immunity
- L21724: `diseaseres`  # Disease immunity

### `displaced`

- L40876: `displaced 1`
- L41040: `displaced 1`
- L41127: `displaced 1`
- L41181: `displaced 1`
- L41264: `displaced 1`
- L44673: `displaced`
- L45319: `displaced 1`
- L48720: `displaced`

### `dispossess`

- L11736: `dispossess`
- L18267: `dispossess`

### `dmg`

- L3552: `dmg     9999`
- L3594: `dmg 1`
- L4116: `dmg        8`
- L4130: `dmg        6`
- L4137: `dmg        8`
- L4193: `dmg       -50`
- L4224: `dmg        5`
- L4261: `dmg        2`

### `dmgonterr`

- L98: `dmgonterr -1012`
- L38845: `dmgonterr -1010`
- L39105: `dmgonterr -1010`
- L39121: `dmgonterr -1010`
- L39137: `dmgonterr -1010`
- L39153: `dmgonterr -1010`
- L39169: `dmgonterr -1010`
- L39328: `dmgonterr -1010`

### `dmgonterrbonus`

- L99: `dmgonterrbonus 1`
- L38846: `dmgonterrbonus 2`
- L39106: `dmgonterrbonus 2`
- L39122: `dmgonterrbonus 2`
- L39138: `dmgonterrbonus 2`
- L39154: `dmgonterrbonus 2`
- L39170: `dmgonterrbonus 2`
- L39329: `dmgonterrbonus 2`

### `dmgtype`

- L3509: `dmgtype 12`
- L3517: `dmgtype 12`
- L3526: `dmgtype 1`
- L3534: `dmgtype 1`
- L3542: `dmgtype 1`
- L3551: `dmgtype    7`  # Magic
- L3558: `dmgtype    2`  # Blunt
- L3573: `dmgtype   12`  # Special damage (determined by bitmask where this attack is used)

### `drain`

- L4568: `drain`
- L4776: `drain`
- L4880: `drain`
- L8276: `drain`
- L8788: `drain`
- L10784: `drain`
- L10906: `drain`
- L11995: `drain`

### `drawsize`

- L42448: `drawsize 25`
- L49407: `drawsize -33`
- L49554: `drawsize -33`
- L49628: `drawsize 20`
- L49653: `drawsize -20`
- L49704: `drawsize -50`
- L49727: `drawsize -50`
- L49750: `drawsize -50`

### `drown`

- L3576: `drown`  # Doesn't affect beings able to survive in water
- L3648: `drown`  # Doesn't affect beings able to survive in water
- L3664: `drown`  # Doesn't affect beings able to survive in water
- L5660: `drown`
- L5821: `drown`
- L7814: `drown`
- L7988: `drown`
- L13542: `drown`

### `easymr`

- L3661: `easymr`
- L5455: `easymr`
- L5817: `easymr`
- L7325: `easymr`
- L7374: `easymr`
- L7496: `easymr`
- L7542: `easymr`
- L8557: `easymr`

### `eatdead`

- L32417: `eatdead 100`
- L32423: `eatdead 100`
- L42236: `eatdead 25`

### `eatdeadcap`

- L42237: `eatdeadcap 2`

### `eatvillage`

- L47094: `eatvillage       1`
- L47144: `eatvillage       1`
- L47191: `eatvillage       1`
- L47334: `eatvillage       1`
- L47451: `eatvillage       1`
- L47552: `eatvillage       1`
- L47600: `eatvillage       1`
- L47958: `eatvillage       1`

### `enchantedgate`

- L79146: `enchantedgate`
- L79437: `enchantedgate`  # The gate of the fort is enchanted to be more durable. (Glowing crystalline conduits)
- L79453: `enchantedgate`  # The gate of the fort is enchanted to be more durable. (Pulsating energy field)
- L79526: `enchantedgate`  # The gate of the fort is enchanted to be more durable. (Bio-mechanical/crystalline)
- L79541: `enchantedgate`  # The gate of the fort is enchanted to be more durable. (Protective energy field)
- L79708: `enchantedgate`  # Bio-metallic/runic circuitry suggests advanced gate.
- L79912: `enchantedgate`  # The gate of the fort is enchanted to be more durable.
- L79948: `enchantedgate`  # The gate of the fort is enchanted to be more durable.

### `endevent`

- L80528: `endevent`
- L80535: `endevent`
- L80543: `endevent`
- L80570: `endevent`
- L80579: `endevent`
- L80589: `endevent`
- L80600: `endevent`
- L80610: `endevent`

### `ethereal`

- L7624: `ethereal`
- L7638: `ethereal`
- L7652: `ethereal`
- L7671: `ethereal`
- L7690: `ethereal`
- L8303: `ethereal`
- L8321: `ethereal`
- L8339: `ethereal`

### `evasion`

- L35202: `evasion 0`
- L38841: `evasion 1`
- L39101: `evasion 1`
- L39117: `evasion 1`
- L39133: `evasion 1`
- L39149: `evasion 1`
- L39165: `evasion 1`
- L39324: `evasion 1`

### `eventvarreq`

- L65534: `eventvarreq 375`  # must have at least 1 in the migration population pool
- L65560: `eventvarreq 375`  # must have at least 1 in the migration population pool
- L65633: `eventvarreq 375`  # must have at least 1 in the migration population pool
- L65659: `eventvarreq 375`  # must have at least 1 in the migration population pool
- L65711: `eventvarreq 375`  # must have at least 1 in the migration population pool
- L66078: `eventvarreq 375`  # must have at least 1 in the migration population pool
- L72461: `eventvarreq 375`  # must have at least 1 in the migration population pool
- L72486: `eventvarreq 375`  # must have at least 1 in the migration population pool

### `expendable`

- L2433: `expendable 1`
- L2437: `expendable 1`
- L2441: `expendable 1`
- L3188: `expendable 1`
- L26491: `expendable 1`
- L30580: `expendable 0`
- L31239: `expendable 1`
- L31250: `expendable 1`

### `extraeyes`

- L25740: `extraeyes        5`
- L40223: `extraeyes       -1`
- L40242: `extraeyes       -1`
- L40262: `extraeyes       -1`
- L42053: `extraeyes 1`
- L46505: `extraeyes -1`
- L48694: `extraeyes       99`
- L49424: `extraeyes       -1`

### `failplayer`

- L57552: `failplayer 24`  # Failed summons will be owned by this player: Independents
- L57827: `failplayer 24`  # Failed summons will be owned by this player: Independents
- L58800: `failplayer 24`  # Failed summons will be owned by this player: Independents
- L58929: `failplayer 24`  # Failed summons will be owned by this player: Independents
- L59843: `failplayer 25`
- L60001: `failplayer 25`
- L60721: `failplayer 25`  # Failed summons will be owned by this player: Special Monsters.
- L60738: `failplayer 25`  # Failed summons will be owned by this player: Special Monsters.

### `farsight`

- L32809: `farsight 1`
- L32815: `farsight 1`
- L42732: `farsight 1`
- L53623: `farsight 1`
- L53633: `farsight 1`
- L79139: `farsight`
- L79162: `farsight`
- L79198: `farsight`

### `farsummon`

- L57629: `farsummon`
- L59920: `farsummon`
- L61387: `farsummon`  # The ritual will summon the monsters specified in a random string at target location instead of at the caster's location.
- L61406: `farsummon`  # The ritual will summon the monsters specified in a random string at target location instead of at the caster's location.
- L64001: `farsummon`
- L64210: `farsummon`
- L64638: `farsummon`
- L64676: `farsummon`

### `farvis`

- L79992: `farvis`  # Can be seen from far away (3 squares?).
- L85318: `farvis`

### `fast`

- L31191: `fast`
- L31490: `fast`
- L31517: `fast`
- L31540: `fast`
- L32814: `fast`
- L35669: `fast`
- L39382: `fast`
- L39395: `fast`

### `fastheal`

- L25006: `fastheal`
- L25015: `fastheal`
- L25018: `fastheal`
- L25021: `fastheal`
- L25024: `fastheal`
- L25027: `fastheal`
- L25030: `fastheal`
- L25033: `fastheal`

### `fear`

- L21577: `fear             2`  # Causes Dread (1D8 vs morale) within 2 squares
- L21607: `fear             2`  # Causes Dread (1D8 vs morale) within 2 squares
- L21638: `fear             2`  # Causes Dread (1D8 vs morale) within 2 squares
- L21663: `fear`  # Causes Fear (1D7 vs morale) in adjacent squares
- L21695: `fear`  # Causes Fear (1D7 vs morale) in adjacent squares
- L21727: `fear`  # Causes Fear (1D7 vs morale) in adjacent squares
- L21760: `fear             2`  # Causes Dread (1D8 vs morale) within 2 squares
- L21792: `fear             2`  # Causes Dread (1D8 vs morale) within 2 squares

### `female`

- L30370: `female`
- L30409: `female`
- L43783: `female`  # Female.
- L43814: `female`  # Female.
- L46414: `female`
- L48745: `female`  # Female.
- L49359: `female`
- L49389: `female`

### `fireaura`

- L22071: `fireaura         5`
- L22133: `fireaura         5`
- L22162: `fireaura         5`
- L42554: `fireaura 1`
- L42588: `fireaura 3`
- L47811: `fireaura 1`
- L47841: `fireaura 2`
- L48155: `fireaura 1`

### `fireexpl`

- L31876: `fireexpl 1`
- L47812: `fireexpl 1`
- L48156: `fireexpl 1`

### `fireres`

- L378: `fireres 20`
- L448: `fireres 20`
- L690: `fireres        -2`  # Fire Immunity
- L21849: `fireres       -100`  # Resistance or vulnerability to fire
- L22062: `fireres        100`  # Fire immunity
- L22103: `fireres         50`  # Resistance or vulnerability to fire
- L22123: `fireres        100`  # Fire immunity
- L22153: `fireres        100`  # Fire immunity

### `firstshape`

- L24430: `firstshape       1`
- L24466: `firstshape       1`
- L31922: `firstshape 1`
- L44245: `firstshape 1`
- L44316: `firstshape 1`
- L49135: `firstshape 1`
- L49168: `firstshape 1`
- L49206: `firstshape 1`

### `float`

- L21564: `float`
- L21593: `float`
- L21624: `float`
- L21653: `float`
- L21684: `float`
- L21716: `float`
- L21746: `float`
- L21778: `float`

### `flying`

- L5533: `flying`
- L5795: `flying`
- L6251: `flying`
- L6965: `flying`
- L6979: `flying`
- L6995: `flying`
- L7011: `flying`
- L7032: `flying`

### `flying2`

- L3436: `flying2`  # 75% chance to not hit.
- L5327: `flying2`
- L12930: `flying2`
- L20367: `flying2`

### `flylook`

- L3562: `flylook  197`
- L3578: `flylook  196`
- L3634: `flylook  197`
- L3650: `flylook  196`
- L3674: `flylook   -1`
- L3687: `flylook    0`
- L3701: `flylook   89`
- L3714: `flylook    0`

### `flymode`

- L3561: `flymode    2`  # Fast particle effect
- L3577: `flymode    8`  # Slow line
- L3633: `flymode    3`  # Fast particle effect
- L3649: `flymode    8`  # Slow line
- L3673: `flymode    0`
- L3700: `flymode    7`  # Line, but single effect even for wide aoe
- L3713: `flymode    2`  # Standard particle effect
- L4120: `flymode    1`  # Missile sprite

### `flysound`

- L3563: `flysound  88`  # water1.wav
- L3579: `flysound  88`  # water1.wav
- L3635: `flysound  88`  # water1.wav
- L3651: `flysound  88`  # water1.wav
- L3675: `flysound 112`  # shortsag.sw
- L3688: `flysound  -1`  # No sound on release
- L3702: `flysound  39`  # snow.sw
- L3715: `flysound  72`  # energy.wav

### `forest`

- L79257: `forest`  # The terrain counts as forest for the purposes of abilities like Forest Stealth.
- L79630: `forest`  # The terrain counts as forest.
- L83682: `forest`
- L83687: `forest`  # turn off to prevent enchant faery circle from being cast on itself.

### `forest1`

- L35447: `forest1`
- L35450: `forest1`
- L35453: `forest1`
- L35462: `forest1`
- L35476: `forest1`
- L35479: `forest1`
- L40518: `forest1`  # Stays in Forest
- L42225: `forest1`

### `forest2`

- L30488: `forest2`  # Prefers Forest
- L35456: `forest2`
- L35483: `forest2`
- L42182: `forest2`
- L56661: `forest2`  # Likes forests (including ancient forests) (if an independent or stupid commander, will not move more than 1 square away from its liked terrains).

### `forestheart`

- L40566: `forestheart      1`  # Takes control of nearby forests

### `foreststealth`

- L27644: `foreststealth`
- L30347: `foreststealth`
- L30381: `foreststealth`
- L30419: `foreststealth`
- L30489: `foreststealth`
- L30699: `foreststealth`
- L31337: `foreststealth`
- L31345: `foreststealth`

### `forgetcurrit`

- L57510: `forgetcurrit`
- L57522: `forgetcurrit`
- L57787: `forgetcurrit`
- L57995: `forgetcurrit`
- L58690: `forgetcurrit`
- L59272: `forgetcurrit`
- L59442: `forgetcurrit`
- L59556: `forgetcurrit`

### `forgetrits`

- L57503: `forgetrits`
- L58017: `forgetrits`
- L58677: `forgetrits`
- L59217: `forgetrits`
- L59236: `forgetrits`
- L60476: `forgetrits`
- L60498: `forgetrits`
- L60702: `forgetrits`

### `free`

- L56946: `free`
- L56958: `free`
- L56971: `free`
- L56993: `free`
- L57528: `free`
- L57541: `free`
- L57580: `free`
- L57622: `free`

### `frontpos`

- L27766: `frontpos`
- L28190: `frontpos`
- L29973: `frontpos`
- L30097: `frontpos`
- L30824: `frontpos`
- L31028: `frontpos`
- L31059: `frontpos`
- L31091: `frontpos`

### `fullsweep`

- L4318: `fullsweep`
- L8898: `fullsweep`
- L15748: `fullsweep`
- L18144: `fullsweep`
- L18739: `fullsweep`
- L20144: `fullsweep`
- L20156: `fullsweep`
- L20189: `fullsweep`

### `fungus`

- L79085: `fungus 1`
- L79097: `fungus 1`
- L79251: `fungus            5`  # Fungus:  7
- L79268: `fungus            5`
- L79626: `fungus            1`  # Fungus:  1
- L79818: `fungus            1`  # Fungus:  1
- L80003: `fungus            2`  # Fungus:  2
- L82660: `fungus 3`

### `gaindarkbless`

- L75621: `gaindarkbless 100`

### `gainrit`

- L57506: `gainrit 1`  # "Steal Son"
- L57585: `gainrit 1`  # "Develop Coal Mine (Slavery)"
- L57783: `gainrit 1`  # "Crossbreeding"
- L57784: `gainrit 2`  # "Improved Crossbreeding"
- L57785: `gainrit -3`  # "Enslave"
- L57803: `gainrit 1`  # "Improved Crossbreeding"
- L58020: `gainrit -1`  # "Study Faery Witch Magic"
- L58072: `gainrit 8`  # "Troll King's Court"

### `gatherfungus`

- L30257: `gatherfungus`
- L30342: `gatherfungus`
- L30372: `gatherfungus`
- L30411: `gatherfungus`
- L30636: `gatherfungus`
- L30640: `gatherfungus`
- L32173: `gatherfungus`
- L32181: `gatherfungus`

### `gathergems`

- L27851: `gathergems`
- L30413: `gathergems`
- L30520: `gathergems`
- L30945: `gathergems`
- L30976: `gathergems`
- L31967: `gathergems`
- L32084: `gathergems`
- L32101: `gathergems`

### `gatherhands`

- L29784: `gatherhands`
- L31363: `gatherhands`
- L32353: `gatherhands`
- L33111: `gatherhands`
- L33114: `gatherhands`
- L33122: `gatherhands`
- L33175: `gatherhands`
- L33184: `gatherhands`

### `gatherherbs`

- L30497: `gatherherbs`
- L30645: `gatherherbs`
- L30812: `gatherherbs`
- L31338: `gatherherbs`
- L31346: `gatherherbs`
- L31354: `gatherherbs`
- L31362: `gatherherbs`
- L32088: `gatherherbs`

### `gatherrelics`

- L39: `gatherrelics`
- L30872: `gatherrelics`
- L30892: `gatherrelics`
- L30910: `gatherrelics`
- L30984: `gatherrelics`
- L30987: `gatherrelics`
- L30990: `gatherrelics`
- L32233: `gatherrelics`

### `gathersacr`

- L30343: `gathersacr`
- L30373: `gathersacr`
- L30412: `gathersacr`
- L30579: `gathersacr`
- L30592: `gathersacr`
- L30946: `gathersacr`
- L30977: `gathersacr`
- L31080: `gathersacr`

### `gatherweed`

- L30644: `gatherweed`
- L31856: `gatherweed`
- L31863: `gatherweed`
- L31870: `gatherweed`
- L32089: `gatherweed`
- L32092: `gatherweed`
- L32096: `gatherweed`
- L32371: `gatherweed`

### `gems`

- L79217: `gems            256`  # Gems: see comments below.
- L79250: `gems           4096`  # Gems: see comments below. # Random gem A    1
- L79267: `gems         8`  # 1 sapphire
- L79315: `gems           4096`  # Random gem A for arcane runes.
- L79327: `gems           4096`  # Random gem A for violet energy/crystalline conduits.
- L79339: `gems            512`  # Emerald for glowing green runic circuitry.
- L79351: `gems              1`  # Ruby for pulsating crimson energy.
- L79362: `gems              8`  # Sapphire for deep blue energy filaments.

### `ghoulify`

- L6851: `ghoulify`
- L11505: `ghoulify`
- L15347: `ghoulify`
- L18177: `ghoulify`

### `gold`

- L118: `gold -3`
- L30441: `gold -1`
- L30466: `gold -1`
- L30657: `gold 3`
- L30871: `gold -5`
- L30891: `gold -3`
- L30909: `gold -2`
- L31216: `gold -1`

### `goldbonus`

- L80070: `goldbonus -5`
- L80076: `goldbonus -30`
- L80082: `goldbonus -25`
- L80088: `goldbonus -15`
- L80094: `goldbonus -20`
- L80100: `goldbonus -25`
- L80106: `goldbonus -22`
- L80112: `goldbonus 0`

### `goldcarrier`

- L30341: `goldcarrier      50`
- L30371: `goldcarrier     100`
- L30410: `goldcarrier     150`
- L31271: `goldcarrier 1`
- L31289: `goldcarrier 1`
- L31698: `goldcarrier    100`
- L31727: `goldcarrier    30`
- L31751: `goldcarrier    100`

### `growhp`

- L43960: `growhp 19`
- L44281: `growhp 125`
- L44352: `growhp 125`
- L45448: `growhp 130`
- L45524: `growhp 90`
- L45554: `growhp 100`
- L45556: `growhp`
- L45566: `growhp 60`

### `growoffs`

- L31460: `growoffs 6`
- L31567: `growoffs -1`
- L31609: `growoffs 2`
- L31630: `growoffs 2`
- L31656: `growoffs -1`
- L31770: `growoffs -1`
- L31824: `growoffs -1`
- L31845: `growoffs -1`

### `growterr`

- L31568: `growterr -32`
- L31657: `growterr -32`
- L31771: `growterr -22`
- L31825: `growterr -22`
- L31846: `growterr -22`
- L33560: `growterr -25`
- L40600: `growterr -25`
- L43001: `growterr -3`

### `growtime`

- L30048: `growtime 10`  # slightly less than a year
- L30064: `growtime 24`  # 2 years and Centaur grows up, much faster than humans
- L30090: `growtime 10`  # slightly less than a year
- L30104: `growtime 36`  # 3 years and Minotaur grows up, much faster than humans
- L30251: `growtime 60`
- L30348: `growtime 120`
- L30382: `growtime 120`
- L30444: `growtime 12`  # 1 year

### `hadesres`

- L37319: `hadesres 80`
- L39505: `hadesres 95`
- L39524: `hadesres 95`
- L39541: `hadesres 90`
- L43576: `hadesres 90`
- L43611: `hadesres 95`
- L43660: `hadesres 100`
- L43675: `hadesres 90`

### `hadeswander`

- L21669: `hadeswander      7`  # Wanders, ghostly, if a commmander controlled by Hades
- L21969: `hadeswander      7`  # Wanders, ghostly, if a commmander controlled by Hades
- L47855: `hadeswander 7`

### `hands`

- L79159: `hands 1`
- L79283: `hands 2`
- L79485: `hands             2`  # Hands:  2 (Spirit weave, more than standard)
- L79520: `hands             2`  # Hands:  2
- L79771: `hands             1`  # Hands:  1
- L80048: `hands             1`  # Hands from forgotten knowledge.
- L82772: `hands 3`
- L82783: `hands 1`

### `hardmorale`

- L4167: `hardmorale`
- L6749: `hardmorale`
- L13323: `hardmorale`
- L15218: `hardmorale`
- L19991: `hardmorale`

### `hardmr`

- L4477: `hardmr`
- L4516: `hardmr`
- L4592: `hardmr`
- L4861: `hardmr`
- L5134: `hardmr`
- L5656: `hardmr`
- L6086: `hardmr`
- L6104: `hardmr`

### `hasportalreq`

- L68465: `hasportalreq           2`

### `healonterr`

- L49968: `healonterr -93`
- L56153: `healonterr 129`  # Manufactury
- L56179: `healonterr 129`  # Manufactury
- L56209: `healonterr 129`  # Manufactury
- L56236: `healonterr 129`  # Manufactury

### `herbs`

- L79086: `herbs 1`
- L79098: `herbs 2`
- L79294: `herbs 4`
- L79702: `herbs             1`  # Herbs:  1 (from bio-regeneration)
- L79817: `herbs             2`  # Herbs:  2
- L79907: `herbs             1`  # Herbs:  1
- L79969: `herbs             2`  # Herbs:  2
- L80004: `herbs             1`  # Herbs:  1

### `hideanimals`

- L31340: `hideanimals`
- L31348: `hideanimals`
- L31356: `hideanimals`
- L31364: `hideanimals`
- L41173: `hideanimals 1`
- L41682: `hideanimals      1`
- L41720: `hideanimals`
- L41753: `hideanimals      1`

### `hoburg`

- L79291: `hoburg`

### `holy`

- L24959: `holy`  # Always blessed
- L24977: `holy`  # Always blessed
- L25280: `holy`
- L43923: `holy`
- L43953: `holy`
- L46338: `holy`
- L46357: `holy`
- L46382: `holy`

### `holykill`

- L7936: `holykill`
- L9160: `holykill`
- L11162: `holykill`
- L16821: `holykill`
- L18050: `holykill`

### `homeplane`

- L43866: `homeplane        9`  # When slain, reforms in Void, controlled by no player
- L47628: `homeplane 5`
- L47656: `homeplane 5`
- L47687: `homeplane 5`

### `hometerr`

- L76330: `hometerr 20`
- L76387: `hometerr 3`
- L76467: `hometerr 3`
- L76532: `hometerr 17`
- L76579: `hometerr 508`
- L76664: `hometerr 206`  # market village
- L76715: `hometerr 30`
- L76812: `hometerr 24`

### `horror`

- L24234: `horror`  # Moves to kill
- L24271: `horror`  # Moves to kill
- L24300: `horror`  # Moves to kill
- L24327: `horror`  # Moves to kill
- L24351: `horror`  # Moves to kill
- L24382: `horror`  # Moves to kill
- L24420: `horror`  # Moves to kill
- L24452: `horror`  # Moves to kill

### `hp`

- L11: `hp 26`
- L14: `hp 20`
- L17: `hp 12`
- L20: `hp 7`
- L23: `hp 10`
- L26: `hp 10`
- L29: `hp 10`
- L32: `hp 10`

### `hpoverflow`

- L32033: `hpoverflow 10`
- L32419: `hpoverflow 20`
- L32425: `hpoverflow 8`
- L37556: `hpoverflow 1`
- L41820: `hpoverflow 95`
- L41853: `hpoverflow 15`
- L42187: `hpoverflow 20`
- L42234: `hpoverflow 50`

### `huge`

- L4155: `huge`
- L4527: `huge`
- L8125: `huge`
- L8582: `huge`
- L8774: `huge`
- L8945: `huge`
- L9521: `huge`
- L10956: `huge`

### `human`

- L22230: `human`
- L24958: `human`
- L24976: `human`
- L24994: `human`
- L30340: `human`
- L30436: `human`
- L30572: `human`
- L30866: `human`

### `humancost`

- L76683: `humancost 999`
- L76773: `humancost 999`
- L78861: `humancost 999`  # Cannot recruit humans at special locations (castles, desert palaces).
- L78884: `humancost         175`
- L78954: `humancost         250`

### `iceprot`

- L32158: `iceprot 1`
- L32167: `iceprot 2`
- L32174: `iceprot 1`
- L32182: `iceprot 2`
- L32852: `iceprot 3`
- L33558: `iceprot 2`
- L33603: `iceprot 3`
- L44242: `iceprot 3`

### `icon`

- L1: `icon "pop/popbanner.tga"`

### `immobile`

- L21437: `immobile`  # Doesn't move in battle
- L21462: `immobile`  # Doesn't move in battle
- L21487: `immobile`  # Doesn't move in battle
- L21512: `immobile`  # Doesn't move in battle
- L21869: `immobile`  # Doesn't move in battle
- L24380: `immobile`  # Doesn't move in battle
- L24820: `immobile`  # Doesn't move in battle
- L24872: `immobile`  # Doesn't move in battle

### `immortal`

- L21693: `immortal`
- L21725: `immortal`
- L21844: `immortal`
- L21879: `immortal`
- L30933: `immortal`
- L31310: `immortal`
- L31315: `immortal`
- L31320: `immortal`

### `immortalap`

- L21851: `immortalap       6`
- L21887: `immortalap       3`
- L30934: `immortalap 8`
- L31311: `immortalap 36`
- L31316: `immortalap 36`
- L31321: `immortalap 24`
- L31327: `immortalap 36`
- L31332: `immortalap 24`

### `inanimate`

- L4159: `inanimate`
- L4188: `inanimate`
- L4203: `inanimate`
- L4418: `inanimate`
- L4435: `inanimate`
- L4524: `inanimate`
- L4570: `inanimate`
- L4778: `inanimate`

### `incorporate`

- L24396: `incorporate      5`
- L24855: `incorporate      2`

### `indepitem`

- L30870: `indepitem      100`
- L30890: `indepitem       50`
- L45152: `indepitem      100`
- L45179: `indepitem       50`
- L45229: `indepitem      100`
- L45261: `indepitem       50`
- L45313: `indepitem      100`
- L45346: `indepitem       50`

### `infwander`

- L21548: `infwander        6`  # Wanders, devilishly, if a commmander controlled by Inferno
- L44382: `infwander        6`
- L50823: `infwander        6`  # Wanders, devilishly, if a commmander controlled by Inferno

### `init`

- L3525: `init 2`
- L3533: `init 2`
- L3541: `init 2`
- L3550: `init       4`
- L3557: `init       4`
- L3572: `init       4`
- L3591: `init 5`
- L3602: `init       4`

### `invert`

- L20987: `invert`

### `invisible`

- L699: `invisible`
- L736: `invisible`
- L21541: `invisible`
- L22348: `invisible`
- L24275: `invisible`
- L24304: `invisible`
- L24388: `invisible`
- L24426: `invisible`

### `iron`

- L76146: `iron 30`
- L79177: `iron 5`
- L79550: `iron              1`  # Iron:  1 (Ancient rock, mining potential)
- L79665: `iron              1`  # Iron:  1
- L79783: `iron              2`  # Iron:  2
- L79808: `iron              1`  # Iron:  1
- L79884: `iron              1`  # From "dark metallic sensor array"
- L83904: `iron 5`

### `ironbonus`

- L80071: `ironbonus 0`
- L80077: `ironbonus 0`
- L80083: `ironbonus 0`
- L80089: `ironbonus 0`
- L80095: `ironbonus 0`
- L80101: `ironbonus 0`
- L80107: `ironbonus 0`
- L80113: `ironbonus 0`

### `ironcarrier`

- L31272: `ironcarrier 1`
- L31290: `ironcarrier 1`
- L38412: `ironcarrier 1`
- L38418: `ironcarrier 2`
- L41399: `ironcarrier 3`
- L41408: `ironcarrier 2`
- L41418: `ironcarrier 1`
- L41481: `ironcarrier 3`

### `irongate`

- L79185: `irongate`
- L79203: `irongate`
- L79589: `irongate`  # The gate of the fort is iron.
- L79688: `irongate`  # The gate of the fort is iron.
- L79761: `irongate`  # Dark metallic plates, bio-mechanical.
- L79789: `irongate`  # The gate of the fort is iron
- L80020: `irongate`  # The gate of the fort is iron
- L85725: `irongate`

### `jungle1`

- L35473: `jungle1`
- L42227: `jungle1`

### `jungle2`

- L24672: `jungle2`  # Prefers jungles
- L24697: `jungle2`  # Prefers jungles
- L30545: `jungle2`  # Prefers Jungle
- L42184: `jungle2`

### `killtarg`

- L56945: `killtarg            9999`  # Automatically kills target unit
- L57183: `killtarg 9999`
- L57481: `killtarg 9999`
- L57664: `killtarg 9999`
- L58144: `killtarg 9999`
- L58531: `killtarg 4`
- L58680: `killtarg 9999`
- L58735: `killtarg 2`

### `killunit`

- L80707: `killunit 40`
- L80719: `killunit 40`
- L80731: `killunit 40`
- L80742: `killunit 40`
- L86579: `killunit 40`
- L86591: `killunit 40`
- L86603: `killunit 40`
- L86614: `killunit 40`

### `landshape`

- L31167: `landshape -1`
- L31189: `landshape -1`
- L33502: `landshape -1`
- L33519: `landshape -1`
- L33623: `landshape -1`
- L33640: `landshape -1`
- L33659: `landshape -1`
- L33676: `landshape -1`

### `large`

- L3439: `large`
- L4156: `large`
- L5797: `large`
- L10828: `large`
- L10844: `large`
- L13714: `large`
- L18751: `large`
- L18898: `large`

### `largeshield`

- L31742: `largeshield`
- L31787: `largeshield`
- L31813: `largeshield`
- L44009: `largeshield`
- L48000: `largeshield`
- L48235: `largeshield`
- L48309: `largeshield`
- L48455: `largeshield`

### `leadership`

- L25200: `leadership -1`
- L31495: `leadership       1`
- L31523: `leadership       1`
- L31602: `leadership       1`
- L31679: `leadership       2`
- L31798: `leadership 3`
- L31826: `leadership 3`
- L31848: `leadership 3`

### `level`

- L38290: `level 9`
- L56942: `level                  1`
- L56954: `level 4`
- L56967: `level 3`
- L56989: `level 2`
- L57054: `level 3`
- L57074: `level 2`
- L57094: `level 3`

### `levelreq`

- L57492: `levelreq 1`
- L57961: `levelreq 3`
- L57985: `levelreq 3`
- L58007: `levelreq               2`
- L58129: `levelreq 1`
- L58609: `levelreq 2`
- L58669: `levelreq 2`
- L58701: `levelreq 2`

### `levelup`

- L57960: `levelup 4`
- L58709: `levelup 3`
- L59446: `levelup 2`
- L59559: `levelup 3`
- L60648: `levelup 4`
- L61363: `levelup                3`  # Level up to new monster (mastery on monster) if below level 3.
- L61615: `levelup             3`  # Level up to the monster in string if below level 3.
- L61769: `levelup             3`  # Level up to the monster in string if below level 3.

### `levelupmon`

- L70319: `levelupmon 3`  # Level up to the monster in string if below level 3.
- L70344: `levelupmon 3`  # Level up to the monster in string if below level 3.
- L70371: `levelupmon 3`  # Level up to the monster in string if below level 3.
- L70396: `levelupmon 3`  # Level up to the monster in string if below level 3.
- L70576: `levelupmon        2`  # Level up to the monster in string if below level 2.
- L70598: `levelupmon        2`  # Level up to the monster in string if below level 2.
- L70622: `levelupmon        2`  # Level up to the monster in string if below level 2.
- L70647: `levelupmon        2`  # Level up to the monster in string if below level 2.

### `libbonusdescr`

- L78722: `libbonusdescr          "wizards"`
- L78776: `libbonusdescr          "wizards and apprentices"`
- L78865: `libbonusdescr          "wizards and apprentices"`
- L78887: `libbonusdescr          "No human wizards, relies on White Ones"`
- L78958: `libbonusdescr          "No human wizards; relies on Rakshasa sorcery."`

### `libmastery`

- L21671: `libmastery 2`

### `library1`

- L79227: `library1`
- L79318: `library1`  # Arcane runes imply knowledge.
- L79342: `library1`  # Runic circuitry implies knowledge.
- L79412: `library1`  # Rune-etched implies knowledge.
- L79501: `library1`  # Library level +1. (Information hub)
- L79711: `library1`  # Runic circuitry, ancient Xylosian knowledge.
- L79739: `library1`  # Pulsing data-runes.
- L79776: `library1`  # Library level +1.

### `library2`

- L79143: `library2`
- L79213: `library2`
- L79456: `library2`  # Library level +2. (High academic/arcane knowledge)
- L79951: `library2`  # Library level +2.
- L83703: `library2`
- L83706: `library2`
- L83712: `library2`
- L84842: `library2`

### `libraryrec`

- L76364: `libraryrec`
- L76367: `libraryrec`
- L76371: `libraryrec`
- L76563: `libraryrec`
- L76566: `libraryrec`
- L76570: `libraryrec`
- L76690: `libraryrec`
- L76693: `libraryrec`

### `lifeforce`

- L79252: `lifeforce        20`  # 200 Lifeforce can be drained from the square.
- L79269: `lifeforce        20`  # 200 Lifeforce can be drained from the square.
- L79284: `lifeforce 50`
- L79311: `lifeforce        30`  # Moderate lifeforce for an ancient site.
- L79325: `lifeforce        50`  # Colossal, pulsing energy.
- L79337: `lifeforce        40`  # Subtle, shimmering, pulsating field.
- L79349: `lifeforce        30`  # Mystical geo-conduit, pulsating energy.
- L79360: `lifeforce        20`  # Subtly glowing ethereal filaments.

### `likesnorth`

- L78771: `likesnorth          1`  # 1: Willingness to start in the north, on a scale from -10 to 10.
- L78883: `likesnorth         -3`
- L78953: `likesnorth         -3`

### `likessouth`

- L78882: `likessouth          2`
- L78952: `likessouth          2`

### `likesterr`

- L51791: `likesterr -58`

### `likestoburn`

- L27738: `likestoburn 100`
- L30662: `likestoburn 95`
- L30667: `likestoburn 99`
- L46228: `likestoburn 100`

### `limitgold`

- L30783: `limitgold 3`
- L31215: `limitgold        2`
- L31236: `limitgold        3`
- L31391: `limitgold -1`
- L31412: `limitgold -1`
- L31415: `limitgold 15`
- L31498: `limitgold 20`
- L31527: `limitgold 20`

### `limitiron`

- L30784: `limitiron 1`
- L31214: `limitiron        1`
- L32146: `limitiron 3`
- L32155: `limitiron 2`
- L32249: `limitiron 1`
- L32259: `limitiron 2`
- L32305: `limitiron 2`
- L35606: `limitiron -500`

### `lob`

- L4227: `lob`  # Arcing trajectory
- L4608: `lob`  # Arcing trajectory
- L4726: `lob`
- L5015: `lob`
- L5056: `lob`
- L5477: `lob`
- L5971: `lob`
- L9727: `lob`

### `localgoldbonus`

- L56256: `localgoldbonus 5`
- L56272: `localgoldbonus 5`
- L80753: `localgoldbonus 20`
- L80756: `localgoldbonus 40`
- L80759: `localgoldbonus 60`
- L82018: `localgoldbonus 2`

### `localironbonus`

- L80752: `localironbonus 10`
- L80755: `localironbonus 20`
- L80758: `localironbonus 30`

### `localleadership`

- L31496: `localleadership  1`
- L31524: `localleadership  1`
- L31554: `localleadership  1`
- L31584: `localleadership  1`
- L31603: `localleadership  1`
- L31799: `localleadership 5`
- L31827: `localleadership 4`
- L31849: `localleadership 3`

### `look`

- L3564: `look      17`
- L3580: `look      43`
- L3595: `look 1`
- L3605: `look       1`
- L3614: `look       1`
- L3623: `look       1`
- L3636: `look      17`
- L3652: `look      43`

### `lookslike`

- L43432: `lookslike -1`
- L43656: `lookslike -1`
- L43747: `lookslike -1`
- L43869: `lookslike        1`
- L46795: `lookslike 0`
- L49159: `lookslike -1`
- L49194: `lookslike -1`
- L49230: `lookslike -1`

### `lovesterr`

- L51790: `lovesterr -14`
- L51824: `lovesterr -32`

### `lucky`

- L22282: `lucky`  # Has a 50% chance of avoiding damage from any attack
- L38102: `lucky`
- L45318: `lucky`
- L47960: `lucky`
- L51130: `lucky`
- L51174: `lucky`

### `magicshield`

- L32803: `magicshield`
- L40822: `magicshield`
- L40842: `magicshield`
- L56459: `magicshield`  # Reduces damage from most weapons by 0-1; 0-2 against ranged weapons.

### `magicwalls`

- L79542: `magicwalls`  # Ethereal units cannot pass through walls at this fort. (Force field of protective energy)
- L79590: `magicwalls`  # Ethereal units cannot pass through walls at this fort.
- L79836: `magicwalls`  # Crystalline structure, arcane runes, internal luminescence suggests magic defenses
- L79864: `magicwalls`  # Alien technology suggests magic defenses
- L79913: `magicwalls`  # Ethereal units cannot pass through walls at this fort.
- L80021: `magicwalls`  # Ethereal units cannot pass through walls at this fort.
- L85320: `magicwalls`

### `makecolony`

- L40772: `makecolony 107`  # Only the large sized versions make swamps out of plains.
- L42193: `makecolony 36`

### `makeportal`

- L65067: `makeportal          1000`  # Makes a portal at target location with a unique portal number each time the ritual is cast. Portals with the same number link to each other.
- L65070: `makeportal           1000`  # Makes a portal at target location with a unique portal number each time the ritual is cast. Portals with the same number link to each other.
- L68441: `makeportal             2`
- L68459: `makeportal             2`
- L69597: `makeportal          1000`
- L69605: `makeportal          1000`
- L69762: `makeportal          1000`
- L69769: `makeportal          1000`

### `makeruin`

- L24251: `makeruin        10`
- L24361: `makeruin       100`
- L27737: `makeruin 30`
- L30661: `makeruin 5`
- L30666: `makeruin 7`
- L41828: `makeruin 10`
- L41859: `makeruin 1`
- L46211: `makeruin 100`

### `mapfile`

- L7: `mapfile "GOTcoe5.coem"`  # Thanks to Wankovich

### `mastery`

- L21578: `mastery          1`  # Any mastery will be to the unit at this offset
- L21608: `mastery          1`  # Any mastery will be to the unit at this offset
- L21670: `mastery          1`  # Any mastery will be to the unit at this offset
- L21701: `mastery          1`  # Any mastery will be to the unit at this offset
- L21761: `mastery          1`  # Any mastery will be to the unit at this offset
- L22260: `mastery          1`  # Any mastery will be to the unit at this offset
- L24625: `mastery          1`  # Any mastery will be to the unit at this offset
- L24964: `mastery          1`  # Any mastery will be to the unit at this offset

### `maxsinners`

- L21549: `maxsinners      30`
- L44383: `maxsinners      10`
- L50824: `maxsinners      10`

### `maxsum`

- L24252: `maxsum           3`  # This many can be summoned in any one battle

### `meleeambush`

- L32727: `meleeambush 1`
- L32746: `meleeambush 1`
- L41289: `meleeambush 1`
- L41307: `meleeambush 1`
- L41327: `meleeambush 1`
- L41344: `meleeambush 1`
- L41630: `meleeambush 1`
- L42177: `meleeambush 1`

### `meleeweapon`

- L64: `meleeweapon`
- L2303: `meleeweapon 1   490`
- L2310: `meleeweapon 2   490`
- L21536: `meleeweapon        7  10`  # Life Drain (value 7: D7 magic damage)
- L21563: `meleeweapon 10  10`  # Life Drain (value 10: D10 magic damage)
- L21592: `meleeweapon 10  10`  # Life Drain (value 10: D10 magic damage)
- L21623: `meleeweapon 10  10`  # Life Drain (value 10: D10 magic damage)
- L21652: `meleeweapon  3 717`  # Wraithsword (value 3: D13 slash damage)

### `meleeweaponbonus`

- L698: `meleeweaponbonus   2  "Barbed Tail"`
- L22521: `meleeweaponbonus   4 585`  # Illusory Hoof (value 4: D4 blunt damage)
- L23466: `meleeweaponbonus   4 557`  # Phantasmal Hoof (value 4: D4 blunt damage)
- L24013: `meleeweaponbonus   3 565`  # Phantasmal Blast (value 3: D3 magic damage)
- L25535: `meleeweaponbonus  3 177`  # Gusts of Winds (value 3: D3 blunt damage)
- L25541: `meleeweaponbonus        8 177`  # Gusts of Winds (value 8: D8 blunt damage)
- L25546: `meleeweaponbonus 6 180`  # Rumble Earth (value 6: 6 blunt damage)
- L25552: `meleeweaponbonus 12 180`  # Rumble Earth (value 12: 12 blunt damage)

### `meleeweaponlong`

- L22453: `meleeweaponlong  0  583`  # Illusory Pike
- L23401: `meleeweaponlong  0  555`  # Phantasmal Pike
- L25518: `meleeweaponlong  7 518`  # Lesser Flame Strike (value 7: D7 fire damage)
- L25523: `meleeweaponlong 15  81`  # Flame Strike (value 15: D15 fire damage)
- L28567: `meleeweaponlong 1 316`
- L29198: `meleeweaponlong   -1  22`
- L29351: `meleeweaponlong   -1  22`
- L45950: `meleeweaponlong  0  26`

### `meleeweaponspec`

- L22520: `meleeweaponspec   12 584`  # Illusory Lance (value 12: D12 pierce damage)
- L23465: `meleeweaponspec   12 556`  # Phantasmal Lance (value 12: D12 pierce damage)
- L29204: `meleeweaponspec   10  13`
- L29357: `meleeweaponspec    6  13`
- L29362: `meleeweaponspec   10  13`
- L31484: `meleeweaponspec   12  13`
- L31511: `meleeweaponspec   12  13`
- L31547: `meleeweaponspec           12  13`  # Lance Charge: d12 Pierce damage.

### `melt`

- L33557: `melt 2`
- L33601: `melt 12`
- L40583: `melt 2`  # Will slowly die in warmer climates
- L40596: `melt 1`
- L47883: `melt 10`
- L47922: `melt 1`
- L48179: `melt -1`
- L48381: `melt -1`

### `mercboost`

- L77187: `mercboost         -50`  # -50% to frequency of mercenary offers.

### `mercpricemult`

- L76876: `mercpricemult 2`
- L76934: `mercpricemult 2`

### `message`

- L80599: `message -2 "An Arena has produced some income and troops."`
- L80609: `message -2 "An Arena has produced some income and troops."`
- L80619: `message -2 "An Arena has produced some income and troops."`
- L80629: `message -2 "An Arena has produced some income and troops."`
- L80706: `message -2 "A cat familiar has been eaten in a swamp or bog."`
- L80718: `message -2 "A raven familiar has been eaten."`
- L80730: `message -2 "A frog familiar has been eaten."`
- L86516: `message -2 "An Arena has produced some income and troops."`

### `mind`

- L3513: `mind`
- L3521: `mind`
- L4214: `mind`
- L4417: `mind`
- L4434: `mind`
- L4479: `mind`
- L4579: `mind`
- L4594: `mind`

### `mindexpl`

- L24803: `mindexpl         1`

### `mine`

- L79150: `mine`
- L79179: `mine`
- L79258: `mine`  # The terrain counts as a mine.
- L79300: `mine`
- L79800: `mine`  # The terrain counts as a mine.
- L83661: `mine`

### `mines1`

- L56458: `mines1`  # Loves mines (if an independent or stupid commander, will not leave its loved terrains).
- L56597: `mines1`  # Loves mines (if an independent or stupid commander, will not leave its loved terrains).

### `minmonreq`

- L58154: `minmonreq 5`
- L58167: `minmonreq 5`
- L58180: `minmonreq 5`
- L58193: `minmonreq 5`
- L59864: `minmonreq  1`
- L62828: `minmonreq  1`
- L62850: `minmonreq  1`
- L63464: `minmonreq 1`

### `minorstartaff`

- L48013: `minorstartaff 200`

### `mirrorammo`

- L32904: `mirrorammo 10`
- L32909: `mirrorammo 10`
- L32914: `mirrorammo 10`
- L32927: `mirrorammo 100`
- L32930: `mirrorammo 100`
- L32933: `mirrorammo 40`
- L32936: `mirrorammo 30`
- L32939: `mirrorammo 200`

### `mirrortarg`

- L57480: `mirrortarg 4`

### `miscslots`

- L40881: `miscslots`
- L41874: `miscslots`
- L41892: `miscslots`
- L41917: `miscslots`
- L41941: `miscslots`
- L42004: `miscslots`
- L42027: `miscslots`
- L42048: `miscslots`

### `modprio`

- L3: `modprio 5`

### `money1`

- L31050: `money1`
- L31078: `money1`
- L31112: `money1`
- L35502: `money1`
- L35505: `money1`
- L35508: `money1`
- L35511: `money1`
- L35514: `money1`

### `money2`

- L30459: `money2`  # Prefers Gold Income Sites
- L30511: `money2`  # Prefers Gold Income Sites
- L31038: `money2`  # Prefers Gold Income Sites
- L31129: `money2`  # Prefers Gold Income Sites
- L41653: `money2`
- L46254: `money2`
- L46952: `money2`  # Prefers Gold Income Sites

### `monplayerreq`

- L66133: `monplayerreq 1`
- L66167: `monplayerreq 1`

### `mor`

- L375: `mor 6`
- L445: `mor 6`
- L21434: `mor             15`  # Morale
- L21459: `mor             15`  # Morale
- L21484: `mor             15`  # Morale
- L21509: `mor             15`  # Morale
- L21533: `mor              9`  # Morale
- L21560: `mor              8`  # Morale

### `morale`

- L9079: `morale`
- L9105: `morale`
- L9131: `morale`
- L9287: `morale`
- L19970: `morale`
- L19981: `morale`

### `more1spells`

- L380: `more1spells 19`
- L30344: `more1spells 1`
- L30379: `more1spells 1`
- L30416: `more1spells 2`
- L30953: `more1spells                    2`  # Starts with 1 extra level 1 spell of each known school.
- L30979: `more1spells                    2`  # Starts with 1 extra level 1 spell of each known school.
- L32130: `more1spells      2`
- L32145: `more1spells 1`

### `more2spells`

- L30417: `more2spells 1`
- L30954: `more2spells                    1`  # Starts with 1 extra level 2 spell of each known school.
- L30980: `more2spells                    1`  # Starts with 1 extra level 2 spell of each known school.
- L32131: `more2spells      1`
- L35657: `more2spells 4`
- L41018: `more2spells 1`
- L41103: `more2spells 2`
- L41158: `more2spells 1`

### `more3spells`

- L35658: `more3spells 3`
- L41104: `more3spells 1`
- L41243: `more3spells 1`
- L42517: `more3spells 1`
- L42582: `more3spells 1`
- L42624: `more3spells 1`
- L42667: `more3spells 1`
- L42709: `more3spells 1`

### `mountain`

- L32697: `mountain`
- L37317: `mountain`
- L37491: `mountain`
- L37493: `mountain`
- L39539: `mountain`
- L41961: `mountain`
- L43771: `mountain`
- L43805: `mountain`

### `mountain1`

- L35486: `mountain1`

### `mountain2`

- L30458: `mountain2`  # Prefers Mountain
- L30510: `mountain2`  # Prefers Mountain
- L35482: `mountain2`
- L44924: `mountain2`
- L56456: `mountain2`  # Likes mountains (if an independent or stupid commander, will not move more than 1 square away from its liked terrains).
- L56596: `mountain2`  # Likes mountains (if an independent or stupid commander, will not move more than 1 square away from its liked terrains).

### `mr`

- L243: `mr 5`
- L3574: `mr`  # Can be resisted through a hard check against magic resistance
- L3646: `mr`  # Can be resisted through a check against magic resistance
- L3678: `mr`
- L4212: `mr`  # Can be resisted through an easy check against magic resistance
- L4241: `mr`
- L4253: `mr`  # Can be resisted through a check against magic resistance
- L4504: `mr`

### `mundane`

- L3560: `mundane`  # Non-magic. Ethereal beings have a 75% chance to be unaffected
- L3597: `mundane`
- L3631: `mundane`
- L4153: `mundane`  # Non-magic. Ethereal beings have a 75% chance to be unaffected
- L4169: `mundane`
- L4262: `mundane`
- L4549: `mundane`
- L4559: `mundane`

### `mutate`

- L6842: `mutate`
- L7304: `mutate`
- L7403: `mutate`
- L15334: `mutate`
- L15939: `mutate`
- L16189: `mutate`
- L19578: `mutate`

### `name`

- L24940: `name " Priest King"`
- L24943: `name " High Priest of the Sun"`
- L24946: `name " Tribal King"`
- L30033: `name " Centaur"`
- L30073: `name " Minotaur"`
- L30127: `name " Pale One"`
- L30132: `name " Pale One Soldier"`
- L30137: `name " Pale One Slinger"`

### `nametype`

- L22072: `nametype         9`  # Pangaea male
- L22102: `nametype         9`  # Pangaea male
- L22135: `nametype         9`  # Pangaea male
- L22163: `nametype         9`  # Pangaea male
- L22352: `nametype         6`  # Roman male
- L24596: `nametype        34`  # Japanese female
- L24703: `nametype        23`  # Mesoamerican male
- L24731: `nametype        23`  # Mesoamerican male

### `nearby1req`

- L65666: `nearby1req -32`  # village+
- L72585: `nearby1req -32`  # village+
- L75656: `nearby1req -96`  # Must be within 1 Lake
- L76027: `nearby1req -32`  # village+

### `nearby3req`

- L64108: `nearby3req -32`  # village+
- L65595: `nearby3req -32`  # village+
- L72519: `nearby3req -32`  # village+
- L75951: `nearby3req -32`  # village+

### `nearby5req`

- L75557: `nearby5req				-2`

### `nevercold`

- L79738: `nevercold`  # Arcane plasma suggests it won't freeze.
- L79973: `nevercold`  # This square will never get cold.

### `neverturn`

- L44207: `neverturn`
- L44212: `neverturn 1`
- L44568: `neverturn 1`
- L44569: `neverturn`
- L44601: `neverturn`
- L44606: `neverturn 1`
- L44637: `neverturn`
- L44648: `neverturn 1`

### `newclass`

- L76323: `newclass`
- L76378: `newclass`
- L76459: `newclass`
- L76528: `newclass`
- L76575: `newclass`
- L77849: `newclass`
- L77920: `newclass`
- L78094: `newclass`

### `newmonster`

- L24948: `newmonster "Priest King"`
- L24966: `newmonster "High Priest of the Sun"`
- L24984: `newmonster "Tribal King"`  # 999
- L28779: `newmonster "Dragon"`
- L28795: `newmonster "Dragon Hatchling"`
- L30035: `newmonster "Centaur Offspring"`
- L30050: `newmonster "Young Centaur"`
- L30066: `newmonster "Centaur"`

### `newrit`

- L57962: `newrit 4`
- L57987: `newrit 3`
- L57988: `newrit 2`
- L57989: `newrit 1`
- L58691: `newrit 2`
- L58692: `newrit 1`
- L58717: `newrit 3`
- L59251: `newrit 2`

### `newritpow`

- L56939: `newritpow`
- L56952: `newritpow`
- L57512: `newritpow`
- L57536: `newritpow`
- L57790: `newritpow`
- L57873: `newritpow`
- L58125: `newritpow`
- L58203: `newritpow`

### `newritual`

- L56940: `newritual     "Destroy Chest"`
- L56953: `newritual     "Craft Item of Power (Enchantment)"`
- L56966: `newritual     "Craft Major Magical Item (Enchantment)"`
- L56988: `newritual     "Craft Minor Magical Item (Enchantment)"`
- L57052: `newritual     "Craft Major Magical Item (Death)"`
- L57072: `newritual     "Craft Minor Magical Item (Death)"`
- L57092: `newritual     "Craft Major Magical Item (Druidism)"`
- L57111: `newritual     "Craft Minor Magical Item (Druidism)"`

### `newspell1`

- L57507: `newspell1 41`  # Troll magic
- L58982: `newspell1 60`
- L58983: `newspell1 60`
- L60482: `newspell1 54`
- L60932: `newspell1 53`
- L60933: `newspell1 53`
- L60935: `newspell1 56`
- L60936: `newspell1 56`

### `newspell2`

- L57508: `newspell2 40`  # Witch magic
- L58021: `newspell2 36`
- L58984: `newspell2 60`
- L60483: `newspell2 54`
- L60706: `newspell2 54`
- L60934: `newspell2 53`
- L60937: `newspell2 56`
- L60940: `newspell2 23`

### `newspell3`

- L57786: `newspell3 43`
- L57976: `newspell3 36`
- L57977: `newspell3 40`
- L58985: `newspell3 60`
- L60663: `newspell3 36`
- L60664: `newspell3 54`
- L66897: `newspell3 23`
- L67545: `newspell3 26`

### `newunits`

- L80527: `newunits -3 "2*Heavy Infantry Guard & 20*Archer Guard"`
- L80534: `newunits -3 "10*Brigand Guard & 10*Bandit Guard & 10*Roaming Bandit"`
- L80541: `newunits -3 "4*Princeps Guard"`
- L80542: `newunits -3 "16*Archer Guard"`
- L80596: `newunits -2 "1d6+1*Gladiator"`
- L80597: `newunits -2 "1d6+1*Retiarius"`
- L80606: `newunits -2 "1d5+1*Gladiator"`
- L80607: `newunits -2 "1d5+1*Retiarius"`

### `newweapon`

- L3507: `newweapon "Visions of the Void"`
- L3515: `newweapon "Visions of the Hypercube"`
- L3523: `newweapon "Huge Magical Bite"`
- L3531: `newweapon "Huge Magical Claw"`
- L3539: `newweapon "Huge Magical Talon"`
- L3548: `newweapon "Annihilation"`
- L3555: `newweapon "Tsunami"`  # 178
- L3570: `newweapon "Sailor's Death  "`  # 179

### `next`

- L3567: `next`  # Extra effect if target is affected: 179, Sailor's Death
- L3639: `next`  # Extra effect if target is affected: 179, Sailor's Death
- L3654: `next`
- L4161: `next`
- L4244: `next`
- L4270: `next`
- L4286: `next`
- L4572: `next`

### `nextalwayswep`

- L20307: `nextalwayswep      411`  # Extra effect if target is hit: 411: Fire.

### `nextdmg`

- L3568: `nextdmg   64`  # = 0x40 (Stun)
- L3583: `nextdmg  999`  # D999 magic damage
- L3640: `nextdmg   64`  # = 0x40 (Stun)
- L3655: `nextdmg  999`  # D999 magic damage
- L4245: `nextdmg 64`
- L4269: `nextdmg   8`
- L4287: `nextdmg    7`
- L5152: `nextdmg 20`

### `nexttoo`

- L56964: `nexttoo`
- L56986: `nexttoo`
- L57069: `nexttoo`
- L57109: `nexttoo`
- L57148: `nexttoo`
- L57186: `nexttoo`
- L57205: `nexttoo`
- L57245: `nexttoo`

### `nextwep`

- L20418: `nextwep            896`  # Extra effect if target is affected: 896: extra bleed.
- L20445: `nextwep            896`  # Extra effect if target is affected: 896: extra bleed.
- L20472: `nextwep            896`  # Extra effect if target is affected: 896: extra bleed.
- L20500: `nextwep            896`  # Extra effect if target is affected: 896: extra bleed.
- L20530: `nextwep            896`  # Extra effect if target is affected: 896: extra bleed.
- L20554: `nextwep            896`  # Extra effect if target is affected: 896: extra bleed.
- L20624: `nextwep            174`  # Extra effect if target is affected: Fire
- L20636: `nextwep            175`  # Extra effect if target is affected: cold

### `nobootslots`

- L22533: `nobootslots`
- L23477: `nobootslots`
- L30063: `nobootslots`
- L30674: `nobootslots`
- L30679: `nobootslots`
- L31556: `nobootslots`  # Has no boot slots.
- L31583: `nobootslots`  # Has no boot slots.
- L39667: `nobootslots`

### `nocombat`

- L22350: `nocombat`  # Non-combatant
- L31873: `nocombat`
- L32489: `nocombat`
- L32500: `nocombat`
- L32514: `nocombat`
- L32520: `nocombat`
- L40605: `nocombat`
- L40787: `nocombat`

### `nodemon`

- L57501: `nodemon`
- L62418: `nodemon`
- L63732: `nodemon`
- L69345: `nodemon`
- L69495: `nodemon`
- L69661: `nodemon`
- L72792: `nodemon`
- L73066: `nodemon`

### `nodrown`

- L80033: `nodrown`  # No drowning if over water.

### `noeyes`

- L22213: `noeyes           1`  # Cannot lose any eye
- L22329: `noeyes           1`  # Cannot lose any eye
- L24248: `noeyes           1`  # Cannot lose any eye
- L24397: `noeyes           1`  # Cannot lose any eye
- L25545: `noeyes 1`
- L25551: `noeyes 1`
- L30281: `noeyes           1`  # Cannot lose any eye
- L30303: `noeyes           1`  # Cannot lose any eye

### `nofemale`

- L59215: `nofemale`
- L59235: `nofemale`
- L63920: `nofemale`
- L70987: `nofemale`
- L71030: `nofemale`
- L74894: `nofemale`
- L74912: `nofemale`
- L75075: `nofemale`

### `nofortreq`

- L65921: `nofortreq           2048`  # Caster's location must not have this fort part: iron gate.
- L67171: `nofortreq           2048`  # Caster's location must not have this fort part: iron gate.
- L68476: `nofortreq             16`  # Caster's location must not have this fort part: 16=gate. what equals "walls"

### `noheal`

- L21443: `noheal`  # Never heals
- L21468: `noheal`  # Never heals
- L21493: `noheal`  # Never heals
- L21518: `noheal`  # Never heals
- L30612: `noheal`  # Never Heals
- L33544: `noheal`
- L33599: `noheal`
- L43734: `noheal`  # Never Heals

### `noland`

- L22205: `noland`  # Purely aquatic
- L49957: `noland`  # The monster cannot move onto land.

### `noleader`

- L26062: `noleader`
- L26075: `noleader`
- L26078: `noleader`
- L30814: `noleader`
- L31872: `noleader`
- L32478: `noleader`
- L32482: `noleader`
- L32490: `noleader`

### `nomonhomereq`

- L57978: `nomonhomereq`
- L58054: `nomonhomereq`  # Monsters in strings beginning with "(-)" must not have their home at target location.
- L58103: `nomonhomereq`  # Monsters in strings beginning with "(-)" must not have their home at target location.
- L58308: `nomonhomereq`
- L58711: `nomonhomereq`
- L59561: `nomonhomereq`
- L60479: `nomonhomereq`
- L60651: `nomonhomereq`

### `nomonplayerreq`

- L66058: `nomonplayerreq 1`
- L69162: `nomonplayerreq 1`
- L72416: `nomonplayerreq 1`
- L72636: `nomonplayerreq 1`
- L72738: `nomonplayerreq 1`

### `nomonreq`

- L58878: `nomonreq`
- L58897: `nomonreq`
- L58976: `nomonreq`
- L58999: `nomonreq`
- L59879: `nomonreq`
- L60551: `nomonreq`  # Monsters in strings beginning with "(-)" must not be here.
- L61655: `nomonreq`
- L61871: `nomonreq`

### `nomonworldreq`

- L60805: `nomonworldreq`
- L69829: `nomonworldreq`
- L69857: `nomonworldreq`
- L71000: `nomonworldreq`  # Monsters in strings beginning with "(-)" must not be anywhere in the world.
- L74923: `nomonworldreq`  # Monsters in strings beginning with "(-)" must not be anywhere in the world.
- L74978: `nomonworldreq 1`
- L75454: `nomonworldreq          1`  # Monsters in strings beginning with "(-)" in the world must be fewer than 1.
- L75805: `nomonworldreq          1`  # Monsters in strings beginning with "(-)" in the world must be fewer than 1.

### `nonearby1req`

- L65230: `nonearby1req 23`
- L65255: `nonearby1req 24`
- L65282: `nonearby1req 26`
- L65309: `nonearby1req 26`
- L65344: `nonearby1req 29`
- L65374: `nonearby1req 29`
- L65403: `nonearby1req 29`
- L65432: `nonearby1req 29`

### `nonearby3req`

- L65621: `nonearby3req -28`  # towns and cities
- L72542: `nonearby3req -28`  # towns and cities
- L75979: `nonearby3req -28`  # towns and cities

### `nonearby5req`

- L59982: `nonearby5req 126`
- L65641: `nonearby5req -113`  # cities
- L72562: `nonearby5req -113`  # cities
- L74939: `nonearby5req 517`  # hoburg city
- L75657: `nonearby5req -25`  # not nearby North
- L76000: `nonearby5req -113`  # cities

### `nonearby7req`

- L66060: `nonearby7req 124`

### `nonearby99req`

- L65697: `nonearby99req 207`
- L76060: `nonearby99req 207`

### `nonmaginvul`

- L21883: `nonmaginvul`  # Invulnerable to non-magical damage
- L44644: `nonmaginvul`
- L47959: `nonmaginvul`

### `nonruin1`

- L52601: `nonruin1`

### `noplanecamo`

- L46959: `noplanecamo -1`

### `north1`

- L35459: `north1`
- L55555: `north1`

### `nosight`

- L79074: `nosight`
- L79084: `nosight`
- L79096: `nosight`
- L79108: `nosight`
- L79118: `nosight`
- L79128: `nosight`
- L79232: `nosight`
- L79260: `nosight`

### `noslots`

- L22099: `noslots`  # No item slots at all
- L22131: `noslots`  # No item slots at all
- L22188: `noslots`  # No item slots at all
- L22351: `noslots`  # No item slots at all
- L24850: `noslots`  # No item slots at all
- L27840: `noslots`
- L30046: `noslots`
- L30087: `noslots`

### `nosnowpen`

- L79077: `nosnowpen`
- L79089: `nosnowpen`
- L79101: `nosnowpen`
- L79111: `nosnowpen`
- L79121: `nosnowpen`
- L79131: `nosnowpen`

### `nostart`

- L38291: `nostart`
- L58696: `nostart`
- L59002: `nostart`
- L59015: `nostart`
- L59250: `nostart`
- L59269: `nostart`
- L60497: `nostart`
- L60845: `nostart`

### `nostdrec`

- L79140: `nostdrec`
- L79163: `nostdrec`
- L79187: `nostdrec`
- L79199: `nostdrec`
- L79216: `nostdrec`
- L83729: `nostdrec`
- L83778: `nostdrec`
- L83814: `nostdrec`

### `nostdtroops`

- L76328: `nostdtroops`
- L76605: `nostdtroops`
- L76639: `nostdtroops`
- L76709: `nostdtroops`
- L76804: `nostdtroops`
- L76886: `nostdtroops`
- L77415: `nostdtroops`
- L77752: `nostdtroops`

### `nostr`

- L4124: `nostr`
- L4411: `nostr`
- L4429: `nostr`
- L4505: `nostr`
- L4523: `nostr`
- L4541: `nostr`
- L4769: `nostr`
- L5354: `nostr`

### `notforpoor`

- L64135: `notforpoor`
- L64148: `notforpoor`
- L64161: `notforpoor`
- L64173: `notforpoor`
- L64185: `notforpoor`
- L64197: `notforpoor`

### `noundead`

- L57500: `noundead`
- L61142: `noundead`
- L62417: `noundead`
- L62674: `noundead`
- L63703: `noundead`
- L63733: `noundead`
- L67971: `noundead`
- L68742: `noundead`

### `nozoc`

- L30047: `nozoc`
- L30088: `nozoc`
- L30439: `nozoc`
- L31432: `nozoc`
- L31456: `nozoc`
- L40604: `nozoc`
- L40649: `nozoc`
- L40686: `nozoc`

### `oneshot`

- L4310: `oneshot`
- L4551: `oneshot`
- L4561: `oneshot`
- L4805: `oneshot`
- L4951: `oneshot`
- L5352: `oneshot`
- L5720: `oneshot`
- L5736: `oneshot`

### `onlyenemy`

- L4157: `onlyenemy`
- L4414: `onlyenemy`
- L4431: `onlyenemy`
- L4507: `onlyenemy`
- L5924: `onlyenemy`
- L5947: `onlyenemy`
- L6870: `onlyenemy`
- L7880: `onlyenemy`

### `onlyfriend`

- L3443: `onlyfriend`
- L3445: `onlyfriend`
- L3447: `onlyfriend`
- L3449: `onlyfriend`
- L3451: `onlyfriend`
- L3453: `onlyfriend`
- L3455: `onlyfriend`
- L3457: `onlyfriend`

### `ornext`

- L57631: `ornext 50`
- L57633: `ornext 95`
- L57635: `ornext 100`
- L57665: `ornext   80`
- L58679: `ornext 50`
- L59934: `ornext 25`
- L59936: `ornext 95`
- L59938: `ornext 100`

### `ornext2`

- L57667: `ornext2  75`
- L57670: `ornext2 75`
- L57673: `ornext2 100`
- L59574: `ornext2 93`
- L66899: `ornext2 20`
- L66932: `ornext2 50`
- L67244: `ornext2 75`
- L67247: `ornext2 75`

### `ornext3`

- L57569: `ornext3 15`
- L57811: `ornext3 10`
- L57839: `ornext3 20`
- L58816: `ornext3 15`
- L59131: `ornext3 3`
- L59166: `ornext3 3`
- L66928: `ornext3 8`
- L67577: `ornext3 8`

### `ornext4`

- L63569: `ornext4 50`
- L70573: `ornext4 5`  # 5.0% chance to levelup2
- L70595: `ornext4 4`  # 4% chance to levelup2
- L70619: `ornext4 1`  # 1% chance to levelup
- L70644: `ornext4 1`  # 1% chance to levelup
- L70670: `ornext4 3`  # 3.0% chance to levelup
- L70694: `ornext4 3`  # 3.0% chance to levelup
- L70736: `ornext4 3`  # 3.0% chance to levelup

### `ornext5`

- L70314: `ornext5 4`  # 4% chance to levelup3 or about 1 year
- L70339: `ornext5 4`  # 4% chance to levelup3 or about 1 year
- L70366: `ornext5 4`  # 4% chance to levelup3 or about 1 year
- L70391: `ornext5 4`  # 4% chance to levelup3 or about 1 year
- L72745: `ornext5 100`

### `otherplanar`

- L76357: `otherplanar`
- L76834: `otherplanar`
- L76904: `otherplanar`
- L76945: `otherplanar`
- L77022: `otherplanar`
- L77201: `otherplanar`
- L77438: `otherplanar`
- L77891: `otherplanar`

### `ownable`

- L79073: `ownable`
- L79083: `ownable`
- L79095: `ownable`
- L79107: `ownable`
- L79117: `ownable`
- L79127: `ownable`
- L79138: `ownable`
- L79161: `ownable`

### `passwall`

- L32802: `passwall`
- L34491: `passwall`  # Bitflag21         # Is an illusion/mirror image
- L34493: `passwall`  # Bitflag21         # Is an illusion/mirror image
- L34495: `passwall`  # Bitflag21         # Is an illusion/mirror image
- L34497: `passwall`  # Bitflag21         # Is an illusion/mirror image
- L34499: `passwall`  # Bitflag21         # Is an illusion/mirror image
- L34501: `passwall`  # Bitflag21         # Is an illusion/mirror image
- L34503: `passwall`  # Bitflag21         # Is an illusion/mirror image

### `phantasm`

- L22376: `phantasm        11`  # Referred to by releasephant of mirrors
- L22398: `phantasm        11`  # Referred to by releasephant of mirrors
- L22420: `phantasm        11`  # Referred to by releasephant of mirrors
- L22441: `phantasm        11`  # Referred to by releasephant of mirrors
- L22463: `phantasm        11`  # Referred to by releasephant of mirrors
- L22485: `phantasm        11`  # Referred to by releasephant of mirrors
- L22507: `phantasm        11`  # Referred to by releasephant of mirrors
- L22534: `phantasm        11`  # Referred to by releasephant of mirrors

### `pierceres`

- L21445: `pierceres`  # Pierce resistance
- L21470: `pierceres`  # Pierce resistance
- L21495: `pierceres`  # Pierce resistance
- L21520: `pierceres`  # Pierce resistance
- L21845: `pierceres`  # Pierce resistance
- L21881: `pierceres`  # Pierce resistance
- L22098: `pierceres`  # Pierce resistance
- L24242: `pierceres`  # Pierce resistance

### `planeloc`

- L62592: `planeloc               5`  # Shift target location to same position but on this plane: Hades.
- L69196: `planeloc 2`  # Sky
- L69216: `planeloc 0`  # Elysium
- L72393: `planeloc -8`
- L75828: `planeloc               5`  # e.g. 5 = Hades

### `planereq`

- L57878: `planereq                0`  # elysium only
- L57965: `planereq                0`
- L60117: `planereq               0`  # Can only be cast on this plane: Elysium.
- L60140: `planereq               0`  # Can only be cast on this plane: Elysium.
- L60182: `planereq               0`  # Can only be cast on this plane: Elysium.
- L60534: `planereq                0`  # elysium only
- L60576: `planereq 0`
- L60627: `planereq 0`

### `planeshift`

- L21576: `planeshift       1`  # Can Plane Shift to Hades
- L21606: `planeshift       1`  # Can Plane Shift to Hades
- L21637: `planeshift       1`  # Can Plane Shift to Hades
- L21668: `planeshift       1`  # Can Plane Shift to Hades
- L21700: `planeshift       1`  # Can Plane Shift to Hades
- L21732: `planeshift       1`  # Can Plane Shift to Hades
- L21759: `planeshift       1`  # Can Plane Shift to Hades
- L21791: `planeshift       1`  # Can Plane Shift to Hades

### `playerevent`

- L80522: `playerevent`
- L80530: `playerevent`
- L80537: `playerevent`
- L80567: `playerevent`
- L80699: `playerevent`
- L80711: `playerevent`
- L80723: `playerevent`
- L80735: `playerevent`

### `poison`

- L11701: `poison`
- L18630: `poison`
- L20430: `poison`
- L20457: `poison`
- L20484: `poison`
- L20512: `poison`
- L20541: `poison`
- L20565: `poison`

### `poisoncloud`

- L22211: `poisoncloud      2`
- L41823: `poisoncloud 3`
- L41854: `poisoncloud 1`
- L44727: `poisoncloud      3`
- L44746: `poisoncloud      3`
- L47839: `poisoncloud 3`
- L47910: `poisoncloud 1`
- L49193: `poisoncloud 5`

### `poisonexpl`

- L47838: `poisonexpl 10`

### `poisonres`

- L379: `poisonres 25`
- L449: `poisonres 25`
- L697: `poisonres 98`
- L21440: `poisonres      100`  # Poison immunity
- L21465: `poisonres      100`  # Poison immunity
- L21490: `poisonres      100`  # Poison immunity
- L21515: `poisonres      100`  # Poison immunity
- L21566: `poisonres      100`  # Poison immunity

### `poisonspikes`

- L24333: `poisonspikes     5`
- L24827: `poisonspikes     4`
- L86995: `poisonspikes 1`
- L87003: `poisonspikes 1`
- L87011: `poisonspikes 1`
- L87019: `poisonspikes 1`
- L87028: `poisonspikes 1`
- L87037: `poisonspikes 1`

### `pop`

- L79229: `pop 2`
- L79286: `pop 50`
- L79313: `pop               5`  # Minor population for a hub.
- L79684: `pop              20`  # Population level: 20
- L79704: `pop               5`  # Population level:  5 (compact building)
- L79860: `pop              20`  # Population level: 20
- L79944: `pop               5`  # Population level:  5
- L80016: `pop               1`  # Population level:  1

### `port`

- L79387: `port`  # Docking spire implies port functionality.
- L79439: `port`  # Partly Water (ships can enter this terrain).
- L79467: `port`  # Partly Water (ships can enter this terrain).
- L79511: `port`  # Partly Water (ships can enter this terrain).
- L79691: `port`  # Partly Water (ships can enter this terrain).
- L79765: `port`  # Designed to contain a flow, likely near water/fluid, allowing ship movement.

### `portalroom`

- L75242: `portalroom 50`

### `power`

- L2304: `power 30 1`
- L2308: `power 30 2`
- L2371: `power 30 3`
- L2375: `power 30 3`
- L21575: `power        1   1`  # Necromancy at level 1
- L21604: `power        1   2`  # Necromancy at level 2
- L21635: `power        1   3`  # Necromancy at level 3
- L21757: `power        1   2`  # Necromancy at level 2

### `prebatweapon`

- L24293: `prebatweapon 5 728`  # Dreamless Sleep (value 5: sleep)
- L24374: `prebatweapon  262144 494`  # Total Confusion (value 262144: =x40000 (Confusion))
- L27577: `prebatweapon       1 513`
- L27710: `prebatweapon      12 370`
- L27717: `prebatweapon 1 371`  # Nerfs Duke of Hell's succubus summon from 3 to only ever 1.
- L27728: `prebatweapon      40 265`
- L27729: `prebatweapon      40 266`
- L28572: `prebatweapon  262144 494`

### `primable`

- L49253: `primable 1`
- L49268: `primable 1`
- L49283: `primable 1`
- L49303: `primable 1`
- L49321: `primable 1`
- L49337: `primable 1`
- L49362: `primable 1`
- L49392: `primable 1`

### `promote`

- L80569: `promote 1 "Duke of Hell Projection"`
- L86209: `promote 1 "Knight"`
- L86227: `promote 1 "Knight"`
- L86245: `promote 1 "Knight"`
- L86263: `promote 1 "Knight"`
- L86295: `promote 1 "Baronet"`
- L86309: `promote 1 "Knight"`
- L86323: `promote 1 "Sea Captain"`

### `promoteunits`

- L86208: `promoteunits -2 1 "Captain" "Knight"`
- L86226: `promoteunits -2 1 "Captain" "Knight"`
- L86244: `promoteunits -2 1 "Captain" "Knight"`
- L86262: `promoteunits -2 1 "Captain" "Knight"`
- L86278: `promoteunits -2 1 "High Lord" "Baronet"`
- L86294: `promoteunits -2 1 "Captain" "Baronet"`
- L86308: `promoteunits -2 1 "Captain" "Knight"`
- L86322: `promoteunits -2 1 "Captain" "Sea Captain"`

### `promotion`

- L57178: `promotion -1`
- L57524: `promotion 1`
- L57661: `promotion 1`
- L58044: `promotion -1`
- L58071: `promotion -1`
- L58119: `promotion -1`
- L58403: `promotion             5`  # promotion units and set target unit to a promotiond unit. Valid promotions are in paired strings not beginning with "(-)".
- L58433: `promotion             5`  # promotion units and set target unit to a promotiond unit. Valid promotions are in paired strings not beginning with "(-)".

### `putcorpses`

- L58926: `putcorpses 125`
- L58954: `putcorpses 50`

### `raiseanimals`

- L62311: `raiseanimals`
- L62467: `raiseanimals`

### `raisedead`

- L62263: `raisedead`
- L62310: `raisedead`  # Raises dead at the current location.
- L62466: `raisedead`
- L62560: `raisedead`  # Raises dead at the current location.
- L62892: `raisedead`  # Raises dead at the current location.

### `randnewloc`

- L58843: `randnewloc             4`  # Ancient forests
- L63828: `randnewloc 79`

### `randomitem`

- L21546: `randomitem      25`
- L21666: `randomitem      10`
- L21698: `randomitem      10`
- L21730: `randomitem      10`
- L30683: `randomitem 1`
- L30687: `randomitem 5`
- L30690: `randomitem 3`
- L30693: `randomitem 7`

### `randomloc`

- L60374: `randomloc              1`  # Sets target location to a random place on the map as follows: land location
- L61373: `randomloc              3`  # Sets target location to a random place on the map as follows: location of random enemy commander.
- L62570: `randomloc              2`  # Sets target location to a random place on the map as follows: location with many corpses (excluding present).
- L69601: `randomloc              1`
- L71888: `randomloc              2`  # Sets target location to a random place on the map as follows: location with many corpses (excluding present).
- L74708: `randomloc              1`  # Sets target location to a random place on the map as follows: random land location.

### `randommisc`

- L31792: `randommisc      20`
- L31818: `randommisc      20`
- L31842: `randommisc      20`
- L31994: `randommisc      50`
- L42524: `randommisc      50`
- L44276: `randommisc      50`
- L44347: `randommisc      50`
- L44724: `randommisc      50`

### `randomrare`

- L30697: `randomrare`
- L30703: `randomrare 10`
- L30707: `randomrare`
- L30711: `randomrare`
- L30715: `randomrare 1`
- L30719: `randomrare 1`
- L30723: `randomrare 1`
- L30727: `randomrare`

### `randomweapon`

- L27676: `randomweapon   100`
- L31697: `randomweapon    50`

### `randterrloc`

- L65069: `randterrloc              53`  # Magma
- L69766: `randterrloc           230`  # pyramids beyond
- L72378: `randterrloc 68`  # Deep sea
- L72394: `randterrloc 68`

### `range`

- L3510: `range 2`
- L3518: `range 3`
- L3524: `range 2`
- L3532: `range 2`
- L3540: `range 2`
- L3549: `range 0`
- L3556: `range 0`
- L3571: `range 6`

### `rangedweapon`

- L273: `rangedweapon 30 237`  # Boulder (value 30: D30 blunt damage)
- L277: `rangedweapon 25 238`  # Boulders (value 25: D25 blunt damage)
- L22366: `rangedweapon 0 577`  # Illusory Bow
- L22739: `rangedweapon 8 592`  # Illusory Burst (value 8: D8 magic damage)
- L22763: `rangedweapon      10 594`  # Illusory Flames (value 10: D10 magic damage)
- L22786: `rangedweapon 8 592`  # Illusory Burst (value 8: D8 magic damage)
- L22809: `rangedweapon      15 593`  # Illusory Blast (value 15: D15 magic damage)
- L22832: `rangedweapon 8 592`  # Illusory Burst (value 8: D8 magic damage)

### `rangedweapon25`

- L27760: `rangedweapon25     6  49`
- L37240: `rangedweapon25 6 "Astral Arrow"`
- L39416: `rangedweapon25 6 "Astral Arrow"`
- L40442: `rangedweapon25 1 "Throwing Dagger"`
- L40443: `rangedweapon25 0 "Throwing Dagger"`
- L41911: `rangedweapon25  8 "Large Tail Sweep"`
- L43149: `rangedweapon25 6 "Astral Arrow on Pegasus"`
- L43180: `rangedweapon25 6 "Astral Arrow"`

### `rangedweapon50`

- L22252: `rangedweapon50     7 306`  # Mind Blast (value 7: D7 magic damage)
- L22276: `rangedweapon50     7 306`  # Mind Blast (value 7: D7 magic damage)
- L27570: `rangedweapon50     1 512`
- L27958: `rangedweapon50     5  46`
- L28149: `rangedweapon50     4 678`
- L28791: `rangedweapon50     6  85`
- L29037: `rangedweapon50     1  78`
- L31877: `rangedweapon50 4 "Project Fire"`

### `rangedweapon50x`

- L28741: `rangedweapon50x         10  85`  # Fiery Breath: d10 Fire damage.
- L28749: `rangedweapon50x         10  38`  # Poison Breath: d10 Poison damage.
- L28757: `rangedweapon50x         10 276`  # Icy Breath: d10 Cold damage.
- L28765: `rangedweapon50x         10 858`  # Lightning Breath: d10 Shock damage.

### `rangedweaponbonus`

- L22180: `rangedweaponbonus  1 407`  # Enslave (value 1: enslave)
- L22202: `rangedweaponbonus  8 721`  # Mind Tentacles (value 8: D8 magic damage)
- L22860: `rangedweaponbonus 12 593`  # Illusory Blast (value 12: D12 magic damage)
- L22861: `rangedweaponbonus  9 594`  # Illusory Flames (value 9: D9 magic damage)
- L23237: `rangedweaponbonus 15 593`  # Illusory Blast (value 15: D15 magic damage)
- L23288: `rangedweaponbonus 999 599`  # Illusory Death (value 999: D999 magic damage)
- L23289: `rangedweaponbonus  20 592`  # Illusory Burst (value 20: D20 magic damage)
- L23290: `rangedweaponbonus  15 593`  # Illusory Blast (value 15: D15 magic damage)

### `rangepen`

- L4119: `rangepen`  # Damage penalty at long range
- L4264: `rangepen`
- L4609: `rangepen`  # Damage penalty at long range
- L4728: `rangepen`
- L4760: `rangepen`
- L4995: `rangepen`
- L5017: `rangepen`
- L5058: `rangepen`

### `rank`

- L1512: `rank 1`
- L21430: `rank`  # Mid
- L21455: `rank`  # Mid
- L21480: `rank`  # Mid
- L21505: `rank`  # Mid
- L21529: `rank`  # Mid
- L21556: `rank            -1`  # Back
- L21585: `rank            -1`  # Back

### `rare`

- L79330: `rare`  # Colossal ancient structure.
- L79367: `rare`  # Ethereal Filament Bar sounds rare.
- L79377: `rare`  # Ancient, alien rock formation.
- L79400: `rare`  # Psionic Shard Beach implies rarity.
- L79424: `rare`  # Gravitational flux anomaly implies rarity.
- L79575: `rare`  # The terrain is rare.
- L79619: `rare`  # The terrain is rare.
- L79633: `rare`  # The terrain is rare.

### `rarestart`

- L57095: `rarestart`
- L57114: `rarestart`
- L57173: `rarestart`
- L57190: `rarestart`
- L57209: `rarestart`
- L57271: `rarestart`
- L57289: `rarestart`
- L57309: `rarestart`

### `realport`

- L79319: `realport`  # Functions as a transport hub, like a realport for ships.
- L79692: `realport`  # Ships can be recruited here.

### `reanimate`

- L6108: `reanimate`
- L7916: `reanimate`
- L8164: `reanimate`
- L9233: `reanimate`
- L9531: `reanimate`
- L11435: `reanimate`
- L14408: `reanimate`
- L16571: `reanimate`

### `rearpos`

- L22462: `rearpos`  # Seeks position to the rear within its rank
- L22986: `rearpos`  # Seeks position to the rear within its rank
- L23409: `rearpos`  # Seeks position to the rear within its rank
- L23912: `rearpos`  # Seeks position to the rear within its rank
- L27604: `rearpos`
- L30055: `rearpos`
- L30080: `rearpos`
- L30451: `rearpos`

### `rebatelvl`

- L57519: `rebatelvl 2`
- L58746: `rebatelvl 3`
- L60399: `rebatelvl              3`
- L60425: `rebatelvl              3`
- L60548: `rebatelvl 3`
- L60562: `rebatelvl 3`
- L60610: `rebatelvl 3`
- L61011: `rebatelvl 2`

### `rebateterr20`

- L57474: `rebateterr20 -56`
- L57545: `rebateterr20 -64`
- L57772: `rebateterr20 -56`
- L57894: `rebateterr20 -20`  # Swamp bog
- L58300: `rebateterr20 3`
- L58357: `rebateterr20 167`
- L58400: `rebateterr20 3`  # at temple city
- L58430: `rebateterr20 3`  # at temple city

### `rebateterr50`

- L57475: `rebateterr50 156`
- L57546: `rebateterr50 -13`
- L57773: `rebateterr50 -57`  # Magic Library 3
- L57895: `rebateterr50         -20`  # Swamp bog
- L57934: `rebateterr50 223`  # Arcane nexus (reduces cost for ether variants)
- L58208: `rebateterr50 32`
- L58239: `rebateterr50 515`
- L58269: `rebateterr50 131`

### `recasschance`

- L76642: `recasschance 2`
- L76751: `recasschance       2`
- L76808: `recasschance       2`
- L76888: `recasschance       2`
- L76947: `recasschance       2`
- L77034: `recasschance       6`
- L77435: `recasschance       2`
- L77773: `recasschance       2`

### `recherochance`

- L76641: `recherochance 1`
- L76749: `recherochance      1`
- L76887: `recherochance      1`
- L76946: `recherochance      1`
- L77036: `recherochance      1`
- L77150: `recherochance      2`
- L77267: `recherochance      1`
- L77348: `recherochance      1`

### `reclimiter`

- L76365: `reclimiter "+Engineer"`
- L76368: `reclimiter "+Master Engineer"`
- L76372: `reclimiter "+Master Engineer"`
- L76425: `reclimiter  "-Tribal Prince"`
- L76427: `reclimiter  "-Lion King"`
- L76429: `reclimiter  "-Slave Queen"`
- L76433: `reclimiter  "-Tribal King"`
- L76435: `reclimiter  "-Tribal Queen"`

### `recterr`

- L77538: `recterr      102`
- L77541: `recterr      102`
- L77544: `recterr      102`
- L77663: `recterr 32`
- L77666: `recterr 516`
- L77669: `recterr 131`
- L77993: `recterr 32`
- L77996: `recterr 516`

### `recwizchance`

- L76640: `recwizchance 0`
- L76755: `recwizchance       1`
- L77885: `recwizchance -100`
- L78105: `recwizchance -1000`
- L80290: `recwizchance -100`
- L80294: `recwizchance -100`
- L80298: `recwizchance -100`
- L80302: `recwizchance -100`

### `recxcost`

- L76854: `recxcost 5  10`  # 10 Hands additional cost.
- L76857: `recxcost 5   5`  # 5 Hands additional cost.
- L76974: `recxcost 3  50`  # fungus additional cost.
- L77054: `recxcost 4  25`  # sacr additional cost.
- L77291: `recxcost 2 50`
- L77388: `recxcost 7 4`
- L77394: `recxcost 8 4`
- L77400: `recxcost 9 4`

### `reducetown`

- L57571: `reducetown`
- L57608: `reducetown`
- L57813: `reducetown`
- L57841: `reducetown`
- L58818: `reducetown`
- L58924: `reducetown`
- L58952: `reducetown`
- L59133: `reducetown`

### `reformdestroy`

- L27939: `reformdestroy  2`
- L41050: `reformdestroy 50`
- L41190: `reformdestroy 50`

### `reformloc`

- L21854: `reformloc     1000`  # When slain, reforms in home square
- L21890: `reformloc     1000`  # When slain, reforms in home square
- L30935: `reformloc 1000`
- L31312: `reformloc     16`
- L31317: `reformloc     16`
- L31322: `reformloc     16`
- L31328: `reformloc     16`
- L31333: `reformloc     16`

### `regeneration`

- L23975: `regeneration`
- L24065: `regeneration`
- L25009: `regeneration`
- L25012: `regeneration`
- L25039: `regeneration`
- L25042: `regeneration`
- L25048: `regeneration`
- L25063: `regeneration`

### `reload1`

- L3430: `reload1`
- L3433: `reload1`
- L3679: `reload1`
- L3692: `reload1`
- L4117: `reload1`  # It takes 1 round to reload it
- L4180: `reload1`  # It takes 1 round to reload it
- L4196: `reload1`  # It takes 1 round to reload it
- L4457: `reload1`

### `reload2`

- L4508: `reload2`
- L4542: `reload2`
- L4599: `reload2`
- L5323: `reload2`
- L8504: `reload2`
- L9446: `reload2`
- L9466: `reload2`
- L9486: `reload2`

### `reload3`

- L3587: `reload3`
- L3638: `reload3`
- L3705: `reload3`
- L4630: `reload3`
- L8569: `reload3`
- L12927: `reload3`
- L14444: `reload3`
- L18660: `reload3`

### `resreq`

- L63755: `resreq 1048576`  # caster must be immortal
- L70832: `resreq 1048576`  # caster must be immortal

### `resrestrict`

- L57499: `resrestrict      1048576`  # Caster must not be immortal.
- L57779: `resrestrict      1048576`  # Caster must not be immortal.
- L58015: `resrestrict      1048576`  # Caster must not be immortal.
- L58676: `resrestrict      1048576`  # Caster must not be immortal.
- L58971: `resrestrict      1048576`  # Caster must not be immortal.
- L59017: `resrestrict      1048576`  # Caster must not be immortal.
- L60700: `resrestrict      1048576`  # Caster must not be immortal.
- L60825: `resrestrict      1048576`

### `ritpow`

- L57053: `ritpow 1`
- L57073: `ritpow 1`
- L57093: `ritpow 5`
- L57112: `ritpow 5`
- L57134: `ritpow 47`
- L57151: `ritpow 47`
- L57172: `ritpow 4`
- L57189: `ritpow 4`

### `ritrebate`

- L79778: `ritrebate        15`  # All rituals cast on this location will be 15% cheaper.
- L85316: `ritrebate 50`

### `riverdmg`

- L47099: `riverdmg        40`
- L47150: `riverdmg        40`
- L47196: `riverdmg        40`
- L47285: `riverdmg        40`
- L47337: `riverdmg        40`
- L47454: `riverdmg        40`
- L47521: `riverdmg        40`
- L47557: `riverdmg        40`

### `sacr`

- L79160: `sacr 2`
- L79486: `sacr              1`  # Sacrifices:  1 (Small amount for spectral interaction)
- L79519: `sacr              3`  # Sacrifices:  3 (Higher for an alignment temple)
- L82771: `sacr 8`
- L82779: `sacr 2`
- L83866: `sacr 1`
- L83953: `sacr 1`
- L83986: `sacr 1`

### `sacrscale`

- L62867: `sacrscale`  # Scale summoning amount with sacrifice production of target square.
- L63271: `sacrscale`  # Scale summoning amount with sacrifice production of target square.
- L71287: `sacrscale`
- L71327: `sacrscale`
- L71741: `sacrscale`
- L72531: `sacrscale`
- L74040: `sacrscale`
- L74094: `sacrscale`

### `saner`

- L21605: `saner            1`  # Regains this much sanity per month
- L21636: `saner            2`  # Regains this much sanity per month
- L21758: `saner            1`  # Regains this much sanity per month
- L21790: `saner            2`  # Regains this much sanity per month
- L21852: `saner            5`  # Regains this much sanity per month
- L21888: `saner            5`  # Regains this much sanity per month
- L24652: `saner            1`  # Regains this much sanity per month
- L30937: `saner 1`

### `scatter`

- L4631: `scatter`
- L5325: `scatter`
- L7418: `scatter`
- L9603: `scatter`
- L9633: `scatter`
- L9663: `scatter`
- L10670: `scatter`
- L12929: `scatter`

### `scryloc`

- L58844: `scryloc                1`  # Scry radius 1.5 around target location.
- L60375: `scryloc               15`  # Scry radius 1.5 around target location.
- L60870: `scryloc 200`
- L60893: `scryloc 1000`
- L61374: `scryloc                5`  # Scry radius 0.5 around target location.
- L62571: `scryloc               15`  # Scry radius 1.5 around target location.
- L62593: `scryloc               15`  # Scry radius 1.5 around target location.
- L63106: `scryloc 25`

### `secondshape`

- L24465: `secondshape      1`
- L24499: `secondshape      1`
- L31947: `secondshape 1`
- L44279: `secondshape 1`
- L44350: `secondshape 1`
- L51893: `secondshape      1`
- L51957: `secondshape      1`
- L52028: `secondshape      1`

### `seduceaura`

- L32590: `seduceaura 4`
- L32600: `seduceaura 3`
- L42840: `seduceaura 5`
- L47341: `seduceaura 3`
- L47366: `seduceaura 5`
- L47460: `seduceaura 1`
- L47491: `seduceaura 2`
- L48132: `seduceaura 7`

### `seepast`

- L79364: `seepast`  # Submerged features can offer remote horizon.
- L79388: `seepast`  # Provides remote horizon over water.
- L79440: `seepast`  # Remote Horizon (can see 1 square past this one when adjacent to it).
- L79468: `seepast`  # Remote Horizon (can see 1 square past this one when adjacent to it).
- L79478: `seepast`  # Remote Horizon (can see 1 square past this one when adjacent to it). (Jutting into void)
- L79512: `seepast`  # Remote Horizon (can see 1 square past this one when adjacent to it).
- L79607: `seepast`  # Remote Horizon (can see 1 square past this one when adjacent to it).
- L79693: `seepast`  # Remote Horizon (can see 1 square past this one when adjacent to it).

### `selectclass`

- L76376: `selectclass 13`
- L76457: `selectclass 13`
- L76634: `selectclass 8`
- L76703: `selectclass 1`
- L76798: `selectclass 2`
- L76880: `selectclass 3`
- L76936: `selectclass 4`
- L77011: `selectclass 5`

### `selectmonster`

- L10: `selectmonster "Baron"`
- L13: `selectmonster "High Lord"`
- L16: `selectmonster "King"`
- L19: `selectmonster "Princess"`
- L22: `selectmonster "Court Mage"`
- L25: `selectmonster "Magus"`
- L28: `selectmonster "High Magus"`
- L31: `selectmonster "Alchemist"`

### `selectritual`

- L38289: `selectritual 2:"Lesser Ritual of Mastery"`
- L38294: `selectritual "Summon Champion of Fire"`
- L63688: `selectritual "Blood Rite"`
- L70977: `selectritual "Coronation"`
- L71575: `selectritual "Summon Champion of Water"`
- L74277: `selectritual "Demon Summoning"`
- L74281: `selectritual "Imp Summoning"`
- L74285: `selectritual "Greater Demon Summoning"`

### `selectterr`

- L79069: `selectterr 501`
- L79079: `selectterr 502`
- L79091: `selectterr 503`
- L79103: `selectterr 504`
- L79113: `selectterr 505`
- L79123: `selectterr 506`
- L79134: `selectterr 507`
- L79154: `selectterr 508`  # Bandit Fort

### `selectterrgroup`

- L20786: `selectterrgroup -1000`
- L20795: `selectterrgroup -1001`
- L20808: `selectterrgroup -1002`
- L20815: `selectterrgroup -1003`
- L20825: `selectterrgroup -1004`
- L20832: `selectterrgroup -1005`
- L20844: `selectterrgroup -1006`
- L20852: `selectterrgroup -1007`

### `selectweapon`

- L3429: `selectweapon 688`
- L3432: `selectweapon 502`
- L3435: `selectweapon 98`  # Drop Boulder
- L3438: `selectweapon 742`
- L3442: `selectweapon 214`
- L3444: `selectweapon 320`
- L3446: `selectweapon 321`
- L3448: `selectweapon 374`

### `semistupid`

- L46388: `semistupid 1`
- L51787: `semistupid`
- L51821: `semistupid`

### `sensedead`

- L1676: `sensedead 1`
- L21579: `sensedead        1`
- L21609: `sensedead        1`
- L21639: `sensedead        1`
- L21667: `sensedead        1`
- L21699: `sensedead        1`
- L21731: `sensedead        1`
- L21763: `sensedead        1`

### `setclassname`

- L76324: `setclassname     "Adventuring Company"`
- L76379: `setclassname     "Blood Tide (NPC)"`
- L76460: `setclassname     "Slave King (NPC)"`
- L76529: `setclassname     "Independent Town (NPC)"`
- L76576: `setclassname     "Bandit King (NPC)"`
- L76638: `setclassname     "Republic"`
- L76708: `setclassname "Monarchy"`
- L76800: `setclassname "Thanatocracy"`

### `setcreator`

- L40723: `setcreator       1`

### `setmaincom`

- L76329: `setmaincom "Hero"`
- L76381: `setmaincom       "Statue of the Bloody Mother"`
- L76462: `setmaincom       "Tribal King"`
- L76531: `setmaincom       "Hero"`
- L76578: `setmaincom       "Bandit King"`
- L76659: `setmaincom "Tribune"`
- L76725: `setmaincom       "Baron"`
- L76811: `setmaincom       "Necromancer"`

### `setname`

- L20787: `setname "Caves"`
- L20796: `setname "Towns and Ports"`
- L20809: `setname "Hoburg Settlements smaller than city"`
- L20816: `setname "Hoburg Settlements and Graveyards except clouds"`
- L20826: `setname "Plain and Savanna"`
- L20833: `setname "Temple city, tribal and tent villages"`
- L20845: `setname "Spider tribe villages"`
- L20853: `setname "Savanna and Jungles"`

### `setplane`

- L65068: `setplane 8`
- L69195: `setplane 2`  # sky
- L69215: `setplane 0`  # Elysium
- L69599: `setplane               3`
- L69764: `setplane               4`
- L72377: `setplane 8`
- L72401: `setplane 0`  # Elysium
- L74707: `setplane               4`  # Randomloc etc. will use this plane: Inferno.

### `setplayer`

- L57627: `setplayer 24`
- L59918: `setplayer 24`
- L61386: `setplayer 			  26`  # Horrors
- L63998: `setplayer 24`
- L64209: `setplayer 24`
- L64637: `setplayer 24`
- L64675: `setplayer 24`
- L64721: `setplayer 24`

### `settlement`

- L79228: `settlement`
- L79690: `settlement`  # Defines the terrain as a human settlement.
- L79865: `settlement`  # Defines the terrain as a human settlement.
- L79950: `settlement`  # Defines the terrain as a human settlement.
- L83172: `settlement`
- L83269: `settlement`
- L83842: `settlement`
- L83850: `settlement`

### `shardexpl`

- L32851: `shardexpl 8`
- L33555: `shardexpl 5`
- L33597: `shardexpl 5`
- L45557: `shardexpl 2`
- L45567: `shardexpl 1`
- L45695: `shardexpl        6`
- L45733: `shardexpl        6`
- L47882: `shardexpl 3`

### `shield`

- L22397: `shield`
- L22419: `shield`
- L22532: `shield`
- L23344: `shield`
- L23366: `shield`
- L23476: `shield`
- L31386: `shield`
- L31492: `shield`

### `shieldneg`

- L4969: `shieldneg`
- L5123: `shieldneg`
- L5889: `shieldneg`
- L5910: `shieldneg`
- L6724: `shieldneg`
- L6734: `shieldneg`
- L7735: `shieldneg`
- L7747: `shieldneg`

### `shipmove`

- L49958: `shipmove`  # Monster is a ship. Movement will cost 1 AP for everyone in the same square.

### `shockaura`

- L22100: `shockaura        5`
- L25533: `shockaura  1`
- L25539: `shockaura  2`
- L43875: `shockaura 4`

### `shockres`

- L22095: `shockres       100`  # Shock immunity
- L24459: `shockres       100`  # Shock immunity
- L24854: `shockres        50`  # Resistance to shock
- L25738: `shockres        50`  # Resistance to shock
- L26989: `shockres       -1`  # Shock Immunity
- L26991: `shockres       -1`  # Shock Immunity
- L26993: `shockres       -1`  # Shock Immunity
- L26996: `shockres       -1`  # Shock Immunity

### `shrinkhp`

- L31538: `shrinkhp 15`
- L31641: `shrinkhp 8`
- L31750: `shrinkhp 11`
- L31797: `shrinkhp 16`
- L31823: `shrinkhp 11`
- L43162: `shrinkhp 11`
- L43317: `shrinkhp 12`
- L43514: `shrinkhp 11`

### `siegeweapon`

- L27767: `siegeweapon  40 "Huge Drop Boulder"`
- L28191: `siegeweapon  30  "Large Drop Boulder"`
- L28568: `siegeweapon 3 316`
- L28654: `siegeweapon       20 237`
- L28660: `siegeweapon 25 238`  # Boulders (value 25: D25 blunt damage)
- L28667: `siegeweapon 30 237`  # Boulder (value 30: D30 blunt damage)
- L28836: `siegeweapon       13 237`
- L29414: `siegeweapon  20  "Drop Boulder"`

### `simulacrum`

- L72790: `simulacrum`  # Creates a simulacrum.

### `size1x1`

- L30345: `size1x1`
- L31951: `size1x1`
- L43885: `size1x1`

### `size2x2`

- L21447: `size2x2`  # Size on battlefield (overrides sprite size)
- L21472: `size2x2`  # Size on battlefield (overrides sprite size)
- L21497: `size2x2`  # Size on battlefield (overrides sprite size)
- L21522: `size2x2`  # Size on battlefield (overrides sprite size)
- L22307: `size2x2`  # Size on battlefield (overrides sprite size)
- L22604: `size2x2`  # Size on battlefield (overrides sprite size)
- L22629: `size2x2`  # Size on battlefield (overrides sprite size)
- L23545: `size2x2`  # Size on battlefield (overrides sprite size)

### `slashres`

- L21880: `slashres`  # Slash resistance
- L22097: `slashres`  # Slash resistance
- L24241: `slashres`  # Slash resistance
- L24848: `slashres`  # Slash resistance
- L30514: `slashres`  # Slash Resistance
- L30555: `slashres`
- L32562: `slashres`
- L32794: `slashres`

### `sleepres`

- L21442: `sleepres`  # Sleep immunity
- L21467: `sleepres`  # Sleep immunity
- L21492: `sleepres`  # Sleep immunity
- L21517: `sleepres`  # Sleep immunity
- L21569: `sleepres`  # Sleep immunity
- L21598: `sleepres`  # Sleep immunity
- L21629: `sleepres`  # Sleep immunity
- L21658: `sleepres`  # Sleep immunity

### `slow`

- L22203: `slow`
- L22254: `slow`
- L22278: `slow`
- L24325: `slow`
- L24750: `slow`
- L24774: `slow`
- L24796: `slow`
- L30296: `slow`

### `smoke`

- L79151: `smoke`
- L79204: `smoke`
- L79304: `smoke`
- L79354: `smoke`  # Crimson energy could be hot, creating smoke-like effects.
- L79425: `smoke`  # Ethereal energy causing distortions could look like smoke.
- L79441: `smoke`  # Pixels with a certain pink color (245,0,255) will produce smoke. Pixels with color (235,0,255) will produce flames and smoke. (For pulsing energy)
- L79464: `smoke`  # Pixels with a certain pink color (245,0,255) will produce smoke. Pixels with color (235,0,255) will produce flames and smoke. (For luminous orange liquid)
- L79490: `smoke`  # Pixels with a certain pink color (245,0,255) will produce smoke. Pixels with color (235,0,255) will produce flames and smoke. (For ethereal wisps)

### `snow`

- L31178: `snow`
- L31192: `snow`
- L33540: `snow`
- L33583: `snow`
- L38663: `snow`  # -1 AP to enter snow-covered squares.
- L38674: `snow`  # -1 AP to enter snow-covered squares.
- L38753: `snow`  # -1 AP to enter snow-covered squares.
- L38764: `snow`  # -1 AP to enter snow-covered squares.

### `snowok`

- L79259: `snowok`  # Income in this terrain is not affected by snow.
- L79274: `snowok`  # Income in this terrain is not affected by snow.
- L79658: `snowok`  # Income in this terrain is not affected by snow.
- L79803: `snowok`  # Income in this terrain is not affected by snow.
- L79889: `snowok`  # "Snow-capped" implies cold resistance

### `snowstealth`

- L47678: `snowstealth`
- L55548: `snowstealth`
- L55559: `snowstealth`

### `sound`

- L3529: `sound 1`
- L3537: `sound 1`
- L3545: `sound 1`
- L3565: `sound     89`  # water2.wav
- L3581: `sound     89`  # water2.wav
- L3596: `sound    105`  # whip2.sw
- L3606: `sound     -1`  # No sound on impact
- L3615: `sound     -1`  # No sound on impact

### `soundfx`

- L57497: `soundfx               57`
- L57521: `soundfx               56`  # Sound effect when the ritual is cast: echo.wav.
- L57550: `soundfx               22`  # Sound effect when the ritual is cast: fear
- L57570: `soundfx 16`
- L57573: `soundfx               22`  # Sound effect when the ritual is cast: fear
- L57587: `soundfx               22`  # Sound effect when the ritual is cast: fear
- L57607: `soundfx 16`
- L57618: `soundfx               26`

### `south1`

- L35465: `south1`
- L35469: `south1`
- L44003: `south1`
- L44043: `south1`
- L44079: `south1`
- L44117: `south1`
- L44166: `south1`
- L55573: `south1`

### `spawn1d6mon`

- L31045: `spawn1d6mon 5`
- L31075: `spawn1d6mon 10`
- L31106: `spawn1d6mon 25`
- L40402: `spawn1d6mon 25`
- L40774: `spawn1d6mon 25`  # 25% chance to spawn 1d6 smaller versions over 3 months then eventually shrink into a small one itself.
- L46363: `spawn1d6mon 5`
- L49543: `spawn1d6mon 100`

### `spawnmon`

- L31044: `spawnmon 25`
- L31074: `spawnmon 75`
- L31105: `spawnmon 100`
- L33605: `spawnmon 1`
- L40585: `spawnmon 2`
- L41448: `spawnmon 0`
- L41473: `spawnmon 0`
- L41511: `spawnmon 0`

### `spawnoffs`

- L31046: `spawnoffs 3`
- L31076: `spawnoffs 2`
- L31107: `spawnoffs 1`
- L33606: `spawnoffs -1`
- L33682: `spawnoffs 1`
- L33702: `spawnoffs 1`
- L33721: `spawnoffs 1`
- L42235: `spawnoffs -1`

### `spellrange`

- L25123: `spellrange 1`
- L25125: `spellrange 2`
- L25127: `spellrange 1`
- L25129: `spellrange 2`
- L25131: `spellrange 1`
- L25133: `spellrange 2`
- L25135: `spellrange 1`
- L25137: `spellrange 2`

### `spellweapon`

- L376: `spellweapon 19 1`  # Solar Magic at level 1.
- L21535: `spellweapon        1   1`  # Infernal Magic at level 1
- L21562: `spellweapon 38   1`  # Necromancy at level 1
- L21591: `spellweapon 38   2`  # Necromancy at level 2
- L21622: `spellweapon 38   3`  # Necromancy at level 3
- L21651: `spellweapon  8   1`  # Unlife at level 1
- L21682: `spellweapon  8   2`  # Unlife at level 2
- L21714: `spellweapon  8   3`  # Unlife at level 3

### `spellweapon50`

- L25519: `spellweapon50  1   2`  # Pyromancy at level 1
- L25553: `spellweapon50     6  2`  # Geomancy at level 2
- L28734: `spellweapon50 43 3`
- L29097: `spellweapon50      7   2`
- L29102: `spellweapon50      7   2`
- L31987: `spellweapon50 53   2`  # Silver Arcana at level 2
- L31988: `spellweapon50 56   2`  # Gold Arcana at level 2
- L31989: `spellweapon50 23   2`  # Iron Arcana at level 2

### `spellweapon50s`

- L44983: `spellweapon50s    26   2`
- L44985: `spellweapon50s     6   2`

### `spellweaponbonus`

- L21436: `spellweaponbonus   5   2`  # Storm Magic at level 2
- L21461: `spellweaponbonus  47   2`  # Beast Wards at level 2
- L21486: `spellweaponbonus  48   2`  # Warrior Wards at level 2
- L21511: `spellweaponbonus  46   2`  # Maladies at level 2
- L21867: `spellweaponbonus  38   3`  # Necromancy at level 3
- L21868: `spellweaponbonus  38   3`  # Necromancy at level 3
- L22299: `spellweaponbonus  42   1`  # Void Magic at level 1
- L24230: `spellweaponbonus  10   1`  # Foul Magic at level 1

### `spellweaponsingle`

- L29422: `spellweaponsingle 13   1`
- L29423: `spellweaponsingle 21   1`
- L33478: `spellweaponsingle 54 2`  # forest magic
- L53224: `spellweaponsingle  28   2`  # Dark Prayers at level 2
- L53225: `spellweaponsingle  28   1`  # Dark Prayers at level 1
- L53446: `spellweaponsingle  28   2`  # Dark Prayers at level 2

### `spiritsight`

- L41027: `spiritsight`
- L42594: `spiritsight`
- L42636: `spiritsight`
- L42680: `spiritsight`
- L42720: `spiritsight`
- L42764: `spiritsight`
- L42809: `spiritsight`
- L42850: `spiritsight`

### `spr`

- L79070: `spr "pop/map/roads.tga"`
- L79080: `spr "pop/map/forestroads.tga"`
- L79092: `spr "pop/map/jungleroads.tga"`
- L79104: `spr "pop/map/hillroads.tga"`
- L79114: `spr "pop/map/mountainroads.tga"`
- L79124: `spr "pop/map/desertroads.tga"`
- L79135: `spr "pop/map/magiccastle.tga"`
- L79155: `spr "pop/map/banditfort.tga"`

### `spr1`

- L30037: `spr1 "pop/monster/babycen.tga"`
- L30052: `spr1 "pop/monster/ygcentaur01.tga"`
- L30077: `spr1 "pop/monster/babymin.tga"`
- L30094: `spr1 "pop/monster/ygminotaur01.tga"`
- L30318: `spr1 "pop/monster/monster_2030.tga"`
- L30427: `spr1 "pop/monster/babyt.tga"`
- L30448: `spr1 "pop/monster/ygtroll01.tga"`
- L30479: `spr1 "pop/monster/forestking01.tga"`

### `spr2`

- L30038: `spr2 "pop/monster/babycen.tga"`
- L30053: `spr2 "pop/monster/ygcentaur02.tga"`
- L30078: `spr2 "pop/monster/babymin.tga"`
- L30095: `spr2 "pop/monster/ygminotaur02.tga"`
- L30319: `spr2 "pop/monster/monster_2031.tga"`
- L30428: `spr2 "pop/monster/babyt.tga"`
- L30449: `spr2 "pop/monster/ygtroll02.tga"`
- L30480: `spr2 "pop/monster/forestking02.tga"`

### `spread`

- L1514: `spread 8`
- L36188: `spread 4`
- L37580: `spread 2`
- L37616: `spread 2`
- L37627: `spread 2`
- L46526: `spread 1`
- L49360: `spread 1`
- L51732: `spread 1`

### `spreadcold`

- L79657: `spreadcold`  # The terrain square spreads cold around it.

### `squareench`

- L57970: `squareench            11`  # Create enchantment on target location.
- L57971: `squareench             5`  # Create enchantment on target location.
- L58994: `squareench            15`  # Create enchantment on target location.
- L60566: `squareench             2`  # Create enchantment on target location.
- L60657: `squareench            17`  # Create enchantment on target location.
- L60658: `squareench             6`  # Create enchantment on target location.
- L61652: `squareench 12`
- L65053: `squareench             7`

### `squareevent`

- L80573: `squareevent`
- L80584: `squareevent`
- L80592: `squareevent`
- L80602: `squareevent`
- L80612: `squareevent`
- L80622: `squareevent`
- L80669: `squareevent`
- L80678: `squareevent`

### `start`

- L57994: `start`
- L60469: `start`
- L60679: `start`
- L61198: `start`
- L62075: `start`
- L62104: `start`
- L69284: `start`
- L69309: `start`

### `startinsanity`

- L32670: `startinsanity 0`
- L37462: `startinsanity 0`

### `startitem`

- L37609: `startitem "Sphere of Power"`
- L48849: `startitem "Scepter of the Goblin King"`
- L48850: `startitem "Crown of Intimidation"`
- L48851: `startitem "Elven Armor"`
- L48852: `startitem "Ring of Infinite Gold"`
- L54982: `startitem "A Chest Full of Fire"`
- L54986: `startitem "Adept's Spell Scroll"`
- L54990: `startitem "Amulet of Anti Magic"`

### `startplane`

- L76663: `startplane 0`
- L77188: `startplane          3`  # Starting citadel will be on this plane: Agartha.
- L78772: `startplane          2`  # Starting citadel will be on this plane: Sky.

### `stationary`

- L21439: `stationary`  # Doesn't move on world map
- L21464: `stationary`  # Doesn't move on world map
- L21489: `stationary`  # Doesn't move on world map
- L21514: `stationary`  # Doesn't move on world map
- L21871: `stationary`  # Doesn't move on world map
- L24383: `stationary`  # Doesn't move on world map
- L24822: `stationary`  # Doesn't move on world map
- L24874: `stationary`  # Doesn't move on world map

### `stealth`

- L21571: `stealth`
- L21600: `stealth`
- L21631: `stealth`
- L21660: `stealth`
- L21691: `stealth`
- L21723: `stealth`
- L21753: `stealth`
- L21785: `stealth`

### `stone`

- L4419: `stone`
- L4436: `stone`
- L4525: `stone`
- L6774: `stone`
- L13196: `stone`
- L15247: `stone`
- L18648: `stone`
- L18862: `stone`

### `stonebeing`

- L22105: `stonebeing       1`  # Immune to petrification
- L44205: `stonebeing`
- L44559: `stonebeing`
- L44599: `stonebeing`
- L44635: `stonebeing`
- L45068: `stonebeing`
- L45105: `stonebeing`
- L46312: `stonebeing`

### `str`

- L387: `str 3`
- L21435: `str              7`  # Strength
- L21460: `str              7`  # Strength
- L21485: `str              7`  # Strength
- L21510: `str              7`  # Strength
- L21534: `str              5`  # Strength
- L21561: `str              4`  # Strength
- L21590: `str              4`  # Strength

### `strresist`

- L3566: `strresist`
- L3662: `strresist`
- L3691: `strresist`
- L4099: `strresist`
- L4151: `strresist`
- L4254: `strresist`  # Can be resisted through a check against strength
- L4526: `strresist`
- L5509: `strresist`

### `stupid`

- L31132: `stupid`
- L40597: `stupid`
- L41632: `stupid`
- L42179: `stupid`
- L42224: `stupid`
- L46226: `stupid`
- L46365: `stupid`
- L46955: `stupid`

### `subeventvar`

- L65535: `subeventvar 375`
- L65561: `subeventvar 375`
- L65634: `subeventvar 375`
- L65660: `subeventvar 375`
- L65712: `subeventvar 375`
- L66079: `subeventvar 375`
- L72462: `subeventvar 375`
- L72487: `subeventvar 375`

### `sum0chance`

- L56973: `sum0chance 3`
- L56995: `sum0chance 1`
- L57058: `sum0chance 5`
- L57078: `sum0chance 20`
- L57099: `sum0chance 5`
- L57118: `sum0chance 5`
- L57139: `sum0chance 5`
- L57156: `sum0chance 5`

### `sum1chance`

- L38299: `sum1chance 1`
- L56974: `sum1chance 10`
- L56996: `sum1chance 25`
- L57079: `sum1chance 5`
- L57177: `sum1chance 100`
- L57275: `sum1chance 20`
- L57293: `sum1chance 5`
- L57421: `sum1chance 10`

### `sum2chance`

- L58730: `sum2chance 0`  # Failchance
- L59152: `sum2chance 5`
- L62827: `sum2chance 10`
- L62849: `sum2chance 10`
- L63070: `sum2chance 50`
- L66121: `sum2chance 0`
- L66153: `sum2chance 0`
- L67205: `sum2chance 1`

### `sum3chance`

- L58731: `sum3chance 0`  # Failchance
- L66122: `sum3chance 0`
- L66154: `sum3chance 0`
- L67206: `sum3chance 3`
- L71595: `sum3chance 1`
- L72076: `sum3chance 5`

### `sum4chance`

- L58328: `sum4chance 1`
- L58732: `sum4chance 100`
- L66123: `sum4chance 100`
- L66155: `sum4chance 100`

### `summoning`

- L56960: `summoning`
- L56975: `summoning`
- L56997: `summoning`
- L57060: `summoning`
- L57081: `summoning`
- L57101: `summoning`
- L57120: `summoning`
- L57141: `summoning`

### `swallowres`

- L44565: `swallowres`

### `swamp`

- L22255: `swamp`  # Swamp move
- L22279: `swamp`  # Swamp move
- L24751: `swamp`  # Swamp move
- L24775: `swamp`  # Swamp move
- L30346: `swamp`
- L30380: `swamp`
- L30418: `swamp`
- L30542: `swamp`  # Swamp Move

### `swamp1`

- L22182: `swamp1`  # Stays in swamps
- L44004: `swamp1`
- L44044: `swamp1`
- L44080: `swamp1`
- L44118: `swamp1`
- L44167: `swamp1`

### `swamp2`

- L30544: `swamp2`  # Prefers Swamp

### `sweep`

- L3528: `sweep`
- L3536: `sweep`
- L3544: `sweep`
- L3593: `sweep`
- L4332: `sweep`
- L4346: `sweep`
- L4640: `sweep`
- L4921: `sweep`

### `teleport`

- L24421: `teleport`  # Moves like a flyer, plus teleporting in battle
- L24453: `teleport`  # Moves like a flyer, plus teleporting in battle
- L24489: `teleport`  # Moves like a flyer, plus teleporting in battle
- L35668: `teleport`
- L41020: `teleport`
- L41108: `teleport`
- L41161: `teleport`
- L41247: `teleport`

### `teleportloc`

- L57897: `teleportloc            2`  # Teleport caster's entire army to target location.
- L60600: `teleportloc            2`  # Teleport caster's entire army to target location.
- L60615: `teleportloc            2`  # Teleport caster's entire army to target location.
- L60949: `teleportloc            1`  # Teleport caster only
- L60962: `teleportloc            1`  # Teleport caster only
- L60988: `teleportloc            2`  # Teleport all
- L61000: `teleportloc            2`  # Teleport all
- L61087: `teleportloc            1`  # Teleport caster only

### `tempimmune`

- L79320: `tempimmune`  # Advanced tech implies temperature immunity.
- L79332: `tempimmune`  # Bio-metallic alloys imply temperature immunity.
- L79343: `tempimmune`  # Ancient metal obelisk implies temperature immunity.
- L79365: `tempimmune`  # Ancient, alien structure implies temperature immunity.
- L79378: `tempimmune`  # Alien rock implies temperature immunity.
- L79402: `tempimmune`  # Alien formations imply temperature immunity.
- L79413: `tempimmune`  # Bio-metallic stone implies temperature immunity.
- L79426: `tempimmune`  # Anomaly implies temperature immunity.

### `temple`

- L79302: `temple`
- L79528: `temple`  # The terrain counts as a temple.  Also guarantees a minimum Relic income of 2 (before applying bonusrelics, if applicable).
- L85720: `temple`

### `temple2`

- L46974: `temple2`

### `templebonusdescr`

- L78723: `templebonusdescr       "heralds"`
- L78777: `templebonusdescr       ""`
- L78866: `templebonusdescr       ""`
- L78888: `templebonusdescr       "White One recruitment, Jungle Shrines enhance rituals"`
- L78959: `templebonusdescr       "Sacrificial sites enhance dark rituals."`

### `templerec`

- L76792: `templerec`  # Each temple owned increases chance by an undocumented amount.
- L76837: `templerec`
- L76839: `templerec`
- L76842: `templerec`
- L76845: `templerec`
- L76862: `templerec`
- L76864: `templerec`
- L76866: `templerec`

### `terr`

- L56955: `terr -3`
- L56968: `terr -3`
- L56990: `terr -3`
- L57055: `terr -3`
- L57075: `terr -3`
- L57096: `terr 4`
- L57115: `terr 4`
- L57136: `terr -3`

### `terraformfrom`

- L51475: `terraformfrom -87`
- L51483: `terraformfrom 73`

### `terraformto`

- L51474: `terraformto 12`
- L51482: `terraformto 12`

### `terrboost`

- L62605: `terrboost            165`  # Adds 1 to the number of monsters summoned in this terrain: Pyramids.
- L62656: `terrboost             170`  # If done in deep deposits it adds an extra golem
- L62657: `terrboost             171`  # If done in deep deposits it adds an extra golem
- L62658: `terrboost             172`  # If done in deep deposits it adds an extra golem
- L62659: `terrboost             173`  # If done in deep deposits it adds an extra golem
- L62660: `terrboost             174`  # If done in deep deposits it adds an extra golem
- L62661: `terrboost             175`  # If done in deep deposits it adds an extra golem
- L62662: `terrboost             176`  # If done in deep deposits it adds an extra golem

### `terrscale50`

- L68132: `terrscale50 4`
- L68175: `terrscale50 4`
- L68189: `terrscale50 4`
- L68213: `terrscale50 4`
- L68227: `terrscale50 4`
- L68252: `terrscale50 4`
- L68266: `terrscale50 4`
- L68293: `terrscale50 4`

### `terrstealth`

- L38618: `terrstealth -5`
- L38629: `terrstealth -5`
- L38640: `terrstealth -10`
- L38651: `terrstealth -10`
- L38703: `terrstealth -5`
- L38714: `terrstealth -5`
- L38725: `terrstealth -10`
- L38739: `terrstealth -10`

### `terrstealthinv`

- L38843: `terrstealthinv`
- L39103: `terrstealthinv`
- L39119: `terrstealthinv`
- L39135: `terrstealthinv`
- L39151: `terrstealthinv`
- L39167: `terrstealthinv`
- L39326: `terrstealthinv`
- L39338: `terrstealthinv`

### `thrallhunt`

- L42859: `thrallhunt 20`
- L47102: `thrallhunt       8`
- L47152: `thrallhunt      15`
- L47198: `thrallhunt       8`
- L47339: `thrallhunt       10`
- L47368: `thrallhunt 20`
- L47456: `thrallhunt       6`
- L47560: `thrallhunt 5`

### `townbonusdescr`

- L78886: `townbonusdescr         "Limited trade, few mercenaries"`
- L78957: `townbonusdescr         "No mercenaries; terrorized populace offers little."`

### `trade`

- L30686: `trade 1`
- L40724: `trade 1`
- L79230: `trade 1`
- L79282: `trade 3`
- L79310: `trade             1`  # Trade value for a transport hub.
- L79496: `trade             1`  # Trade:  1 (Data exchange)
- L79584: `trade             1`  # Trade:  1
- L79681: `trade             2`  # Trade:  2

### `trample`

- L22101: `trample          6`
- L23547: `trample          2`
- L24360: `trample         10`
- L27793: `trample 6`
- L27799: `trample 6`
- L27805: `trample 5`
- L27811: `trample 6`
- L27821: `trample 6`

### `tramplexsize`

- L32469: `tramplexsize 1`
- L41915: `tramplexsize -2`
- L41965: `tramplexsize -2`
- L42230: `tramplexsize -1`
- L43872: `tramplexsize -1`

### `transformtarg`

- L57504: `transformtarg 1`
- L57781: `transformtarg 2`
- L58018: `transformtarg 1`
- L58303: `transformtarg 1`
- L58681: `transformtarg 1`
- L58876: `transformtarg 1`
- L58895: `transformtarg 1`
- L58977: `transformtarg 1`

### `treelook`

- L40454: `treelook`

### `trgrank`

- L3508: `trgrank  0`
- L3516: `trgrank  0`
- L3600: `trgrank    0`
- L3609: `trgrank    0`
- L3618: `trgrank    0`
- L3627: `trgrank    1`  # Front row
- L3668: `trgrank    9`  # Any Enemy
- L3682: `trgrank    1`  # Front row

### `troll`

- L30339: `troll            1`
- L30377: `troll            1`
- L30408: `troll            1`
- L30437: `troll 1`
- L30464: `troll            1`
- L30495: `troll            1`
- L30518: `troll            1`
- L56508: `troll 1`

### `tunnel`

- L30276: `tunnel`
- L30297: `tunnel`
- L32801: `tunnel`
- L42800: `tunnel`

### `ug`

- L79671: `ug`  # This is an underground terrain.
- L79802: `ug`  # This is an underground terrain.
- L80042: `ug`  # This is an underground terrain.
- L85821: `ug`  # This is an underground terrain.

### `unaging`

- L693: `unaging`
- L21885: `unaging`  # Decay immunity
- L25366: `unaging`
- L29921: `unaging`
- L29931: `unaging`
- L29942: `unaging`
- L29953: `unaging`
- L29966: `unaging`

### `undead`

- L4160: `undead`
- L4187: `undead`
- L4202: `undead`
- L4416: `undead`
- L4433: `undead`
- L6281: `undead`
- L6302: `undead`
- L6342: `undead`

### `unfollowtarg`

- L72288: `unfollowtarg`
- L73070: `unfollowtarg`
- L73154: `unfollowtarg`
- L73318: `unfollowtarg`
- L74065: `unfollowtarg`

### `unimportant`

- L44209: `unimportant`
- L44564: `unimportant`
- L44603: `unimportant`
- L46271: `unimportant`
- L46291: `unimportant`
- L46314: `unimportant`
- L46478: `unimportant`

### `unique`

- L43865: `unique           1`
- L46169: `unique 1`
- L46209: `unique 1`
- L47948: `unique 1`
- L48698: `unique 1`
- L53125: `unique           1`
- L55781: `unique           1`
- L79189: `unique`

### `updatehome`

- L57777: `updatehome`  # Updates home (immortal resurrection location) for target unit to where he stands.
- L57972: `updatehome`
- L58013: `updatehome`  # Updates home (immortal resurrection location) for target unit to where he stands.
- L58045: `updatehome`
- L58102: `updatehome`  # Updates home
- L58306: `updatehome`
- L59014: `updatehome`  # Updates home (immortal resurrection location) for target unit to where he stands.
- L59443: `updatehome`

### `useable`

- L79329: `useable`  # Portals often imply activation.
- L79344: `useable`  # Territory projector implies an active function.
- L79376: `useable`  # Psionic resonance implies a power that can be activated.
- L79411: `useable`  # Observation implies a function that can be activated.
- L79423: `useable`  # Anomaly implies a power that can be manipulated.
- L79574: `useable`  # There is a special power inherent to the terrain.
- L79618: `useable`  # There is a special power inherent to the terrain.
- L79643: `useable`  # There is a special power inherent to the terrain.

### `varcost`

- L66186: `varcost 50`
- L66251: `varcost 50`
- L66429: `varcost 50`
- L66452: `varcost 50`
- L66482: `varcost 50`
- L66507: `varcost 50`  # Can spend as little as 50% of cost.
- L68735: `varcost 75`
- L68945: `varcost 75`

### `varregen`

- L26507: `varregen 1`
- L26510: `varregen 1`
- L26513: `varregen 2`
- L26516: `varregen 2`
- L38641: `varregen 1`
- L38652: `varregen 1`
- L38726: `varregen 1`
- L38740: `varregen 1`

### `void2`

- L22206: `void2`  # Prefers the Void
- L24753: `void2`  # Prefers the Void
- L24777: `void2`  # Prefers the Void
- L24799: `void2`  # Prefers the Void
- L24823: `void2`  # Prefers the Void

### `voidret`

- L79137: `voidret`
- L79328: `voidret`  # Planar transit implies connection to the Void.
- L79577: `voidret`  # If placed when the map is generated, this terrain will have a one-way portal from the Void.
- L79620: `voidret`  # If placed when the map is generated, this terrain will have a one-way portal from the Void.
- L79644: `voidret`  # If placed when the map is generated, this terrain will have a one-way portal from the Void.
- L79775: `voidret`  # If placed when the map is generated, this terrain will have a one-way portal from the Void.
- L79825: `voidret`  # If placed when the map is generated, this terrain will have a one-way portal from the Void.
- L79839: `voidret`  # Alien origin, arcane runes suggest void connection

### `voidsanity`

- L22212: `voidsanity      20`  # Shield against insanity increases in the void
- L22235: `voidsanity       5`  # Shield against insanity increases in the void
- L22261: `voidsanity      20`  # Shield against insanity increases in the void
- L22284: `voidsanity      20`  # Shield against insanity increases in the void
- L22308: `voidsanity      20`  # Shield against insanity increases in the void
- L22328: `voidsanity      20`  # Shield against insanity increases in the void
- L24249: `voidsanity      20`  # Shield against insanity increases in the void
- L24279: `voidsanity      20`  # Shield against insanity increases in the void

### `wall`

- L22933: `wall`  # Wall climbing
- L23024: `wall`  # Wall climbing
- L23862: `wall`  # Wall climbing
- L23949: `wall`  # Wall climbing
- L24842: `wall`  # Wall climbing
- L30546: `wall`  # Wall Climbing
- L32696: `wall`
- L39662: `wall`  # Wall Climbing

### `walls`

- L79141: `walls`
- L79164: `walls`
- L83726: `walls`

### `wander`

- L31047: `wander 8`
- L31077: `wander 8`
- L31111: `wander 8`
- L46227: `wander 4`
- L47210: `wander 8`
- L51789: `wander 19`
- L51823: `wander 19`
- L55536: `wander 6`

### `wandermaxdist`

- L51788: `wandermaxdist 3`
- L51822: `wandermaxdist 6`
- L56288: `wandermaxdist                  3`  # Maximum distance for raid missions for wanderers.

### `wanderrest`

- L56287: `wanderrest                    80`  # 80% chance for wandering monster to rest a turn instead of going on a mission.

### `water`

- L695: `water`
- L21438: `water`  # Survives/moves in water
- L21463: `water`  # Survives/moves in water
- L21488: `water`  # Survives/moves in water
- L21513: `water`  # Survives/moves in water
- L21836: `water`  # Survives/moves in water
- L21870: `water`  # Survives/moves in water
- L22204: `water`  # Survives/moves in water

### `watershape`

- L31155: `watershape 1`
- L31177: `watershape 1`
- L33495: `watershape 1`
- L33513: `watershape 1`
- L33561: `watershape 5`
- L33604: `watershape 2`
- L33617: `watershape 1`
- L33634: `watershape 1`

### `weaponslots`

- L30369: `weaponslots`  # Item slots for a weapon and two misc items, no more
- L30404: `weaponslots`  # Item slots for a weapon and two misc items, no more
- L30462: `weaponslots`  # Item slots for a weapon and two misc items, no more
- L30493: `weaponslots`  # Item slots for a weapon and two misc items, no more
- L30516: `weaponslots`  # Item slots for a weapon and two misc items, no more
- L33437: `weaponslots`
- L33455: `weaponslots`
- L44958: `weaponslots`

### `weed`

- L79293: `weed 6`
- L80782: `weed  -1`
- L81112: `weed  -1`
- L81472: `weed  -1`
- L82209: `weed 1`
- L82729: `weed 2`
- L83654: `weed 2`
- L83658: `weed 2`

### `winteridle`

- L32699: `winteridle`
- L39663: `winteridle`  # Doesn't move on the map during winter
- L39678: `winteridle`  # Doesn't move on the map during winter
- L39700: `winteridle`  # Doesn't move on the map during winter
- L39714: `winteridle`  # Doesn't move on the map during winter
- L42377: `winteridle`  # Doesn't move on the map during winter
- L42488: `winteridle`  # Doesn't move on the map during winter
- L42559: `winteridle`

### `woodencitadel`

- L85621: `woodencitadel`

### `woodengate`

- L79165: `woodengate`
- L79289: `woodengate`
- L83727: `woodengate`
- L83815: `woodengate`

### `yellow`

- L5250: `yellow`
- L12822: `yellow`

