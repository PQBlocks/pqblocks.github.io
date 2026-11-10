import {
  MLKEM768KeyGenLengthVerifier,
  classifyResult,
  summarizeTaxonomy,
} from '@pqblocks/pqc-acvp-runner';

const verifier = new MLKEM768KeyGenLengthVerifier();
const seed = new Uint8Array(64).fill(0x42);
const keys = verifier.keyGen(seed);

console.log(`ML-KEM-768 key generated: pk=${keys.publicKey.length}B, sk=${keys.secretKey.length}B`);
const taxonomy = summarizeTaxonomy([classifyResult({ tcId: 1 }, { matches: true, error: null })]);
console.log('Taxonomy classification:', taxonomy);
