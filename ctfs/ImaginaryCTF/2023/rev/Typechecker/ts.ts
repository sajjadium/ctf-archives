/**
 * Change the flag below until it compiles correctly on TypeScript 5.1.6 :)
 */
const flag = '______________________________________________________________'
/* Do not change anything below */
type UfMzhXneJMxLGLEU = 'eZ!gjyTdSLcJ3{!Y_pTcMqW7qu{cMoyb04JXFHUaXx{8gTCIwIGE-AAWb1_wu32{'
type WhzQNnyJjDsKWyxC = 'HuuMKaxLVHVqC6NSB1Rwl2WC1F7zkxxrxAuZFpPogbBd4LGGgBfK9!eUaaSIuqJK'
type PTaaOqBorswiazoI = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{_-!}'
type mkIyPGrircFSBTcN = 8
type dGJEEVttmoAPpOAN = 67
type mRYJgulPMUCesDht<
	IMGccnTsvjUQLwrf extends string,
	DeCQhpqVREGeRhnA extends string[] = []
> = IMGccnTsvjUQLwrf extends `${infer head}${infer rest}`
	? mRYJgulPMUCesDht<rest, [...DeCQhpqVREGeRhnA, head]>
	: DeCQhpqVREGeRhnA
type itHZcYyBjnhJWiYP<
	pmdPNolgYxglUHyx extends string[],
	BQNzTQZfrJYoMzZV extends number[] = [],
	TkUOlgwCjrqLMqJJ = {}
> = BQNzTQZfrJYoMzZV['length'] extends pmdPNolgYxglUHyx['length']
	? TkUOlgwCjrqLMqJJ
	: itHZcYyBjnhJWiYP<
			pmdPNolgYxglUHyx,
			[...BQNzTQZfrJYoMzZV, any],
			TkUOlgwCjrqLMqJJ & {
				[_ in pmdPNolgYxglUHyx[BQNzTQZfrJYoMzZV['length']]]: BQNzTQZfrJYoMzZV['length']
			}
	  >
type iiFcDFSKUxThWRKY = itHZcYyBjnhJWiYP<mRYJgulPMUCesDht<PTaaOqBorswiazoI>>
type nGWbztcLxfIfhBVp<
	jBtqUiSUoRoNsKbN extends {
		[k in string]: number
	},
	kjEFIDfZbBUWfQDK extends (keyof jBtqUiSUoRoNsKbN)[],
	BjZKAxdRVmfjgXma extends number[] = []
> = BjZKAxdRVmfjgXma['length'] extends kjEFIDfZbBUWfQDK['length']
	? BjZKAxdRVmfjgXma
	: nGWbztcLxfIfhBVp<
			jBtqUiSUoRoNsKbN,
			kjEFIDfZbBUWfQDK,
			[...BjZKAxdRVmfjgXma, jBtqUiSUoRoNsKbN[kjEFIDfZbBUWfQDK[BjZKAxdRVmfjgXma['length']]]]
	  >
type ozvfWBVZaDHpRmwv<ehAViMhMvaHgpnyf, DLFoWEPElDAydhoh> = (<T>() => T extends ehAViMhMvaHgpnyf ? 1 : 2) extends <
	T
>() => T extends DLFoWEPElDAydhoh ? 1 : 2
	? true
	: false
type cFTwHJlaNLUidmbU<QjZYcNISkUIPleAj extends unknown[]> = QjZYcNISkUIPleAj[0]
type vHbSPTAtgxnHjiGT<BEQYeYFiitEfVaco extends unknown[]> = [any, ...BEQYeYFiitEfVaco][BEQYeYFiitEfVaco['length']]
type OzJOdJrhEGbsCPUc<
	kgZLOXOFncQCkPjp extends unknown[],
	HhkTgnzLBfGczWPO extends number,
	eBCAQjxoeKZLOxyu extends unknown[] = []
> = eBCAQjxoeKZLOxyu['length'] extends HhkTgnzLBfGczWPO
	? eBCAQjxoeKZLOxyu
	: OzJOdJrhEGbsCPUc<
			kgZLOXOFncQCkPjp,
			HhkTgnzLBfGczWPO,
			[...eBCAQjxoeKZLOxyu, kgZLOXOFncQCkPjp[eBCAQjxoeKZLOxyu['length']]]
	  >
type awbCxBeAysbLgqmY<
	QRfOcXtdwaJxcVmW extends unknown[],
	BrJPlsgOrMXoujsc extends number,
	ZNcEIwAnyRFRSfgy extends unknown[] = []
> = ZNcEIwAnyRFRSfgy['length'] extends BrJPlsgOrMXoujsc
	? ZNcEIwAnyRFRSfgy
	: awbCxBeAysbLgqmY<
			QRfOcXtdwaJxcVmW,
			BrJPlsgOrMXoujsc,
			[[...ZNcEIwAnyRFRSfgy, any, ...QRfOcXtdwaJxcVmW][QRfOcXtdwaJxcVmW['length']], ...ZNcEIwAnyRFRSfgy]
	  >
type mDZrKsdAzdETRPHd<EsMccyWXwNPXAgZh extends unknown[], bvUdzEyPoSzYOTDD extends number> = [
	vHbSPTAtgxnHjiGT<EsMccyWXwNPXAgZh>,
	...OzJOdJrhEGbsCPUc<EsMccyWXwNPXAgZh, bvUdzEyPoSzYOTDD>
]
type yhWKIpZaWwaBMLwX<mSVeraqQKHiHIQbO extends unknown[], FJrsjarSYxPPUIxq extends number> = [
	...awbCxBeAysbLgqmY<mSVeraqQKHiHIQbO, FJrsjarSYxPPUIxq>,
	cFTwHJlaNLUidmbU<mSVeraqQKHiHIQbO>
]
type otztzlVJHDvjsfPu<
	uBdxhwacrRHWgpMQ extends number,
	fTZiKZGTXNWUpRBg extends unknown[] = []
> = uBdxhwacrRHWgpMQ extends fTZiKZGTXNWUpRBg['length']
	? fTZiKZGTXNWUpRBg
	: otztzlVJHDvjsfPu<uBdxhwacrRHWgpMQ, [...fTZiKZGTXNWUpRBg, fTZiKZGTXNWUpRBg['length']]>
type heMRZHsxnppbrDuK<
	bVJbiyLabCOwLRXr,
	XBIzKSKknFDmbNnV extends unknown[] = [],
	PSjZkmgMDtZqebJd = {}
> = XBIzKSKknFDmbNnV['length'] extends bVJbiyLabCOwLRXr
	? PSjZkmgMDtZqebJd
	: heMRZHsxnppbrDuK<
			bVJbiyLabCOwLRXr,
			[...XBIzKSKknFDmbNnV, any],
			PSjZkmgMDtZqebJd & {
				[_ in XBIzKSKknFDmbNnV['length']]: unknown
			}
	  >
// @ts-ignore
type NEnOUqglsCrqzjyt<fvMQKzvNrsfxdxCB extends number> = [any, ...otztzlVJHDvjsfPu<fvMQKzvNrsfxdxCB>][fvMQKzvNrsfxdxCB]
type VGMeBpMFMpFRwaMu = otztzlVJHDvjsfPu<dGJEEVttmoAPpOAN>
type pCjUTYFvoqDGoUOv = yhWKIpZaWwaBMLwX<VGMeBpMFMpFRwaMu, NEnOUqglsCrqzjyt<dGJEEVttmoAPpOAN>>
type dcmdpAZbcGEvKfuH = mDZrKsdAzdETRPHd<VGMeBpMFMpFRwaMu, NEnOUqglsCrqzjyt<dGJEEVttmoAPpOAN>>
type upsrRLshcdvzXpoE<ZrThpoGFxMrHKQpo extends number, UlrjGJKApDlutLtl extends number> = UlrjGJKApDlutLtl extends 0
	? ZrThpoGFxMrHKQpo
	: upsrRLshcdvzXpoE<pCjUTYFvoqDGoUOv[ZrThpoGFxMrHKQpo], dcmdpAZbcGEvKfuH[UlrjGJKApDlutLtl]>
type yikKWBFFXiBLeCXn<
	WTritGxPQRfUOtWz extends number,
	gGUjKjFsxmouUtKQ extends number,
	yfRcrgtxYXROWEln extends number = 0
> = gGUjKjFsxmouUtKQ extends 0
	? yfRcrgtxYXROWEln
	: yikKWBFFXiBLeCXn<
			WTritGxPQRfUOtWz,
			dcmdpAZbcGEvKfuH[gGUjKjFsxmouUtKQ],
			upsrRLshcdvzXpoE<yfRcrgtxYXROWEln, WTritGxPQRfUOtWz>
	  >
type RvStwhjakTfnrhsu<
	HWGVTYOJZpBmTLjx extends unknown[],
	VPuenbVMWvaIFqfG extends number = mkIyPGrircFSBTcN,
	dGJEEVttmoAPpOAN extends number = mkIyPGrircFSBTcN,
	uLkxRrueriHkRRrr extends unknown[][] = [],
	oHOIJtKGmbhoJvkA extends unknown[] = [],
	vRRmWHFnetuznOxN extends unknown[] = []
> = uLkxRrueriHkRRrr['length'] extends VPuenbVMWvaIFqfG
	? uLkxRrueriHkRRrr
	: oHOIJtKGmbhoJvkA['length'] extends dGJEEVttmoAPpOAN
	? RvStwhjakTfnrhsu<
			HWGVTYOJZpBmTLjx,
			VPuenbVMWvaIFqfG,
			dGJEEVttmoAPpOAN,
			[...uLkxRrueriHkRRrr, oHOIJtKGmbhoJvkA],
			[],
			vRRmWHFnetuznOxN
	  >
	: RvStwhjakTfnrhsu<
			HWGVTYOJZpBmTLjx,
			VPuenbVMWvaIFqfG,
			dGJEEVttmoAPpOAN,
			uLkxRrueriHkRRrr,
			[...oHOIJtKGmbhoJvkA, HWGVTYOJZpBmTLjx[vRRmWHFnetuznOxN['length']]],
			[...vRRmWHFnetuznOxN, any]
	  >
type QQPUXWDcCREqQrlf<NqisJnGOjKSSeBPz, MLLTjlNYSoqQCTVP extends number, dGJEEVttmoAPpOAN extends number> = {
	[i in keyof heMRZHsxnppbrDuK<MLLTjlNYSoqQCTVP>]: {
		[j in keyof heMRZHsxnppbrDuK<dGJEEVttmoAPpOAN>]: NqisJnGOjKSSeBPz
	}
}
type nYQyaQTkVVtEqdEn<
	YRWtcUUovuCgOgPd extends ArrayLike<number>,
	MSnUotlTasJajgpJ extends number = 0,
	onIvRCYCcFeXeafa extends unknown[] = []
> = onIvRCYCcFeXeafa['length'] extends YRWtcUUovuCgOgPd['length']
	? MSnUotlTasJajgpJ
	: nYQyaQTkVVtEqdEn<
			YRWtcUUovuCgOgPd,
			upsrRLshcdvzXpoE<MSnUotlTasJajgpJ, YRWtcUUovuCgOgPd[onIvRCYCcFeXeafa['length']]>,
			[...onIvRCYCcFeXeafa, any]
	  >
type IzaaMhORtxCvgQNj<
	uOINRhtbXbrGdyBu extends QQPUXWDcCREqQrlf<number, NveVZtruTxmwCpqe, RAqxYxTXFfWDxlBm>,
	MzVSwBihrIpNZsoP extends QQPUXWDcCREqQrlf<number, RAqxYxTXFfWDxlBm, CNAtqPJppnykIezq>,
	NveVZtruTxmwCpqe extends number = mkIyPGrircFSBTcN,
	RAqxYxTXFfWDxlBm extends number = mkIyPGrircFSBTcN,
	CNAtqPJppnykIezq extends number = mkIyPGrircFSBTcN
> = {
	[i in keyof heMRZHsxnppbrDuK<NveVZtruTxmwCpqe>]: {
		[k in keyof heMRZHsxnppbrDuK<CNAtqPJppnykIezq>]: nYQyaQTkVVtEqdEn<
			{
				[j in keyof heMRZHsxnppbrDuK<RAqxYxTXFfWDxlBm>]: yikKWBFFXiBLeCXn<
					uOINRhtbXbrGdyBu[i][j],
					MzVSwBihrIpNZsoP[j][k]
				>
			} & {
				length: RAqxYxTXFfWDxlBm
			}
		>
	}
}
type XtJReCPPCAjRCUxq<WhfLhepBbeZshzhr extends string> = RvStwhjakTfnrhsu<
	nGWbztcLxfIfhBVp<iiFcDFSKUxThWRKY, mRYJgulPMUCesDht<WhfLhepBbeZshzhr>>
>
type ehAViMhMvaHgpnyf = XtJReCPPCAjRCUxq<typeof flag>
function isTheFlagCorrect(
	good: ozvfWBVZaDHpRmwv<
		IzaaMhORtxCvgQNj<XtJReCPPCAjRCUxq<UfMzhXneJMxLGLEU>, ehAViMhMvaHgpnyf>,
		IzaaMhORtxCvgQNj<ehAViMhMvaHgpnyf, XtJReCPPCAjRCUxq<WhzQNnyJjDsKWyxC>>
	>,
	flag: string
) {
	if (/^ictf{.{56}}$/.test(flag) && good) {
		console.log('Correct, the flag is', flag)
	} else {
		console.log('Wrong!')
	}
}
isTheFlagCorrect(true, flag)
