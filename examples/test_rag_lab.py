import unittest
from rag_lab import CORPUS,bm25,eligible,hash_vector,metrics,retrieve,rrf

class RetrievalTests(unittest.TestCase):
    def test_rrf_worked_example(self):
        result=rrf([('A',0),('B',0),('C',0)],[('B',0),('D',0),('A',0)])
        self.assertEqual([x[0] for x in result],['B','A','D','C'])
        self.assertAlmostEqual(dict(result)['A'],1/61+1/63)

    def test_bm25_rare_term_calculation(self):
        from rag_lab import Chunk
        chunks=[Chunk('a','t',('g',),'2027-01-01',None,'carry carry leave','a'),
                Chunk('b','t',('g',),'2027-01-01',None,'leave leave leave','b')]
        import math
        score=dict(bm25('carry',chunks))['a']
        self.assertAlmostEqual(score,math.log(2)*2*2.2/(2+1.2))

    def test_cross_tenant_text_never_enters_candidates_or_evidence(self):
        result=retrieve('PRIVATE OTHER TENANT unused leave')
        self.assertNotIn('other:carry',[key for key,_ in result['fused']])
        self.assertNotIn('PRIVATE OTHER TENANT',str(result['evidence']))

    def test_group_revocation_blocks_evidence(self):
        result=retrieve('unused leave',groups=('unknown',))
        self.assertTrue(result['abstained']);self.assertEqual(result['evidence'],[])

    def test_temporal_half_open_intervals(self):
        old=next(c for c in CORPUS if c.id=='hr42:v2:carry')
        self.assertTrue(eligible(old,'t1',{'employees-pk'},'2026-12-31'))
        self.assertFalse(eligible(old,'t1',{'employees-pk'},'2027-01-01'))
        result=retrieve('carry forward',valid_at='2026-06-01')
        self.assertEqual([x['id'] for x in result['evidence']],['hr42:v2:carry'])

    def test_unknown_terms_abstain_on_bm25(self):
        self.assertEqual(bm25('zzzz_unrelated',CORPUS),[])

    def test_empty_query_abstains_without_zero_division(self):
        self.assertEqual(hash_vector(''),{});self.assertTrue(retrieve('')['abstained'])

    def test_known_query_retrieves_both_required_sources(self):
        result=retrieve('unused leave carry forward')
        self.assertTrue({'hr42:v3:carry','hr42:v3:expiry'} <= {x['id'] for x in result['evidence']})
        for chunk in result['evidence']:
            self.assertEqual(chunk['tenant'],'t1')
            self.assertEqual(chunk['valid_from'],'2027-01-01')

    def test_metric_worked_example(self):
        result=metrics(['a','x','b'],{'a','b','c','d'},3)
        self.assertAlmostEqual(result['precision_at_k'],2/3)
        self.assertEqual(result['recall_at_k'],.5);self.assertEqual(result['reciprocal_rank'],1)

    def test_metrics_no_labels_and_invalid_limits(self):
        self.assertIsNone(metrics([],set(),3)['recall_at_k'])
        with self.assertRaises(ValueError):metrics([],set(),0)
        with self.assertRaises(ValueError):retrieve('leave',limit=0)

if __name__=='__main__':unittest.main()
