import { auditEstate, verifyCertificate } from '@pqblocks/cnsa2-pki-auditor';

// Audit certificate directory or PEM files against CNSA 2.0
const result = await auditEstate({
  paths: [],
  deadline: '2030-12-31',
  scanDate: '2026-11-20',
});

console.log('Audited certificates:', result.summary.total);
console.log('Errors:', result.summary.errors);
