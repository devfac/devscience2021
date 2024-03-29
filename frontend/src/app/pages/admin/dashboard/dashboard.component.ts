import { HttpClient, HttpParams } from '@angular/common/http';
import { AfterViewInit, Component, OnInit } from '@angular/core';
import { QueryParams } from '@app/models/query';
import { parseQueryParams } from '@app/shared/utils';
import { NzMessageService } from 'ng-zorro-antd/message';
import { Subject, BehaviorSubject, Observable } from 'rxjs';
import { first, takeUntil } from 'rxjs/operators';
import { HomeService } from '../home/home.service';
import { CollectionViewer, DataSource } from '@angular/cdk/collections';
import { environment } from '@environments/environment';
import { TotalDash } from '@app/models/dashbord';
import { MentionService } from '../home/mention/mention.service';
import { DashboardService } from './dashboard.service';
import { AuthService } from '@app/services/auth/auth.service';
import { CollegeYearService } from '../home/college-year/college-year.service';
import { ResponseModel } from '@app/models/response';

const BASE_URL = environment.authApiURL;

interface ItemData {
  gender: string;
  name: Name;
  email: string;
}

interface Name {
  title: string;
  first: string;
  last: string;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})
export class DashboardComponent implements OnInit {
 
  totalDas : any = {L1:0, L2:0, L3:0, M:0, PL:0, RL:0, TL:0, PM:0, RM:0, TM:0}
  ds = new MyDataSource(this.http);
  
  percentLicencePassant: any = 0;
  percentLicenceRedoublant: any = 0;
  percentLicenceTriplant: any = 0;

  percentMasterPassant: any = 0;
  percentMasterRedoublant: any = 0;
  percentMasterTriplant: any = 0;


  private destroy$ = new Subject();
  constructor(
    private http: HttpClient,
    private service: DashboardService,
    private serviceCollegeYear: CollegeYearService
  ) {}
  async ngAfterViewInit() {
    
  }

  async ngOnInit() {
    let year = localStorage.getItem('reinscriptioncollegeYear')
    if(year){
      this.totalDas = await this.service.totaldashboard(year).toPromise()
    }else{
      let allYears: ResponseModel = await this.serviceCollegeYear.getDataPromise().toPromise()
      let year = allYears.data[0].title
      this.totalDas = await this.service.totaldashboard(year).toPromise()
    }
    let totalLicence = this.totalDas.L1 + this.totalDas.L2 + this.totalDas.L3
    let totalMaster = this.totalDas.M

    this.percentLicencePassant = this.roundNumber((this.totalDas.PL * 100)/ totalLicence)
    this.percentLicenceRedoublant = this.roundNumber((this.totalDas.RL * 100)/ totalLicence)
    this.percentLicenceTriplant = this.roundNumber((this.totalDas.TL * 100)/ totalLicence)

    this.percentMasterPassant = this.roundNumber((this.totalDas.PM * 100)/ totalMaster)
    this.percentMasterRedoublant = this.roundNumber((this.totalDas.RM * 100)/ totalMaster)
    this.percentMasterTriplant = this.roundNumber((this.totalDas.TM * 100)/ totalMaster)

    document.getElementById(
      'passant_licence'
    )!.style.strokeDasharray = `${this.percentLicencePassant} , 100`;
    document.getElementById(
      'redoublant_licence'
    )!.style.strokeDasharray = `${this.percentLicenceRedoublant} , 100`;
    document.getElementById(
      'triplant_licence'
    )!.style.strokeDasharray = `${this.percentLicenceTriplant} , 100`;

  document.getElementById(
    'passant_master'
  )!.style.strokeDasharray = `${this.percentMasterPassant} , 100`;
  document.getElementById(
    'redoublant_master'
  )!.style.strokeDasharray = `${this.percentMasterRedoublant} , 100`;
  document.getElementById(
    'triplant_master'
  )!.style.strokeDasharray = `${this.percentMasterTriplant} , 100`;
}


  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  fetchData() {
   // return this.homeService.getDataObservable(parseQueryParams(params));
  }
  roundNumber(num: number) {
    if (num.toString().includes('.')) {
      var scale = num.toString().split('.');
      if (scale[1].length > 2) return num.toFixed(2);
    }
    return num;
  }
}

class MyDataSource extends DataSource<ItemData> {
  private pageSize = 10;
  private cachedData: ItemData[] = [];
  private fetchedPages = new Set<number>();
  private dataStream = new BehaviorSubject<ItemData[]>(this.cachedData);
  private complete$ = new Subject<void>();
  private disconnect$ = new Subject<void>();
  constructor(private http: HttpClient) {
    super();
  }

  completed(): Observable<void> {
    return this.complete$.asObservable();
  }

  connect(collectionViewer: CollectionViewer): Observable<ItemData[]> {
    this.setup(collectionViewer);
    return this.dataStream;
  }

  disconnect(): void {
    this.disconnect$.next();
    this.disconnect$.complete();
  }

  private setup(collectionViewer: CollectionViewer): void {
    this.fetchPage(0);
    collectionViewer.viewChange
      .pipe(takeUntil(this.complete$), takeUntil(this.disconnect$))
      .subscribe((range) => {
        if (this.cachedData.length >= 100) {
          this.complete$.next();
          this.complete$.complete();
        } else {
          this.fetchPage(range.end + 1);
        }
      });
  }

  private fetchPage(pageIndex: number): void {
    if (this.fetchedPages.has(pageIndex)) {
      return;
    }
    this.fetchedPages.add(pageIndex);

    let _params: QueryParams = {
      pageIndex: pageIndex + 1,
      pageSize: 10,
      sortField: null,
      sortOrder: null,
    };
    this.fetchData(_params)
      ?.pipe(first())
      .subscribe({
        next: (data) => {
          this.cachedData.splice(pageIndex * this.pageSize, this.pageSize, ...data.data);
          this.dataStream.next(this.cachedData);
        },
      });
    /*
    this.http
      .get<{ results: ItemData[] }>(
        `https://randomuser.me/api/?results=${this.pageSize}&inc=name,gender,email,nat&noinfo`
      )
      .pipe(catchError(() => of({ results: [] })))
      .subscribe((res) => {
        this.cachedData.splice(page * this.pageSize, this.pageSize, ...res.results);
        this.dataStream.next(this.cachedData);
      });
      */
  }
  fetchData(params?: QueryParams) {
    return this.getDataObservable(parseQueryParams(params));
  }
  getDataObservable(params: HttpParams): Observable<any> {
    return this.http.get<any>(`${BASE_URL}/college_year/`,{params: params});
  }

}