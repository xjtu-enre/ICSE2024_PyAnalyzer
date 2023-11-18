import creator from './creator';
import extractor from './extractor';
import builder from './builder';
import {error} from '@pyanalyzer/logging';
import {CaseContainer} from '@pyanalyzer/doc-parser';
import {UNIMatcher} from '../../../matchers';
import {readFile} from 'node:fs/promises';

export default async (g: string, c: string, cs: CaseContainer, ocwd: string, exepath: string) => {
  try {
    const data = await readFile(`${process.cwd()}/tests/pyanalyzer/${g}/${c}/_${c}-report-pyanalyzer.json`, 'utf-8');
    // console.log(data.replaceAll(/\s+/g, ' '));
    builder(data);
    return UNIMatcher(cs, 'python', 'e');
  } catch {
    if (await creator(g, c, exepath)) {
      const data = await extractor(g, c, ocwd);
      if (data) {
        // console.log(data.replaceAll(/\s+/g, ' '));
        builder(data);
        return UNIMatcher(cs, 'python', 'e');
      } else {
        error(`Failed to read pyanalyzer output on ${g}/${c}`);
      }
    } else {
      error(`Failed to execute pyanalyzer on ${g}/${c}`);
    }
  }
};
