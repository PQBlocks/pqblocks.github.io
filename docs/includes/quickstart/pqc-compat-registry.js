import { algorithms, parse_oid, validate_oid, get_oid_by_algorithm,
         validate_parameter_sizes, validate_slh_dsa_sizes, ALL_ALGORITHMS } from '@pqblocks/pqc-compat-registry';

// 1. Look up a parameter set by name
const kem = algorithms['ml-kem-768'];
console.log(kem.oid_dotted);        // '2.16.840.1.101.3.4.4.2'
console.log(kem.key_length);        // 1184 (encapsulation key bytes)
console.log(kem.security_lambda);   // 192

// 2. Parse an OID back to its algorithm
const r = parse_oid('2.16.840.1.101.3.4.3.19');
console.log(r.algorithm);           // 'ml-dsa-87'

// 3. Validate that observed sizes match the FIPS table
console.log(validate_oid('2.16.840.1.101.3.4.4.1'));                 // true
console.log(validate_parameter_sizes('ml-dsa-44',
  { public_key: 2560, private_key: 1312, signature: 2420 }));        // { valid: true, ... }
console.log(validate_slh_dsa_sizes('slh-dsa-sha2-128s',
  { private_key: 64, public_key: 32, signature: 7856 }));            // { valid: true, ... }

// 4. Reverse lookup: name -> OID
console.log(get_oid_by_algorithm('slh-dsa-shake-256f')); // '2.16.840.1.101.3.4.3.31'
console.log(ALL_ALGORITHMS.length);                              // 18
