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
  data = [
    'Racing car sprays burning fuel into crowd.',
    'Japanese princess to wed commoner.',
    'Australian walks 100km after outback crash.',
    'Man charged over missing wedding girl.',
    'Los Angeles battles huge wildfires.',
    'Racing car sprays burning fuel into crowd.',
    'Japanese princess to wed commoner.',
    'Australian walks 100km after outback crash.',
    'Man charged over missing wedding girl.',
    'Los Angeles battles huge wildfires.',
    'Racing car sprays burning fuel into crowd.',
    'Japanese princess to wed commoner.',
    'Australian walks 100km after outback crash.',
    'Man charged over missing wedding girl.',
    'Los Angeles battles huge wildfires.',
  ];
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
    private nzMessage: NzMessageService,
    private mentionService: MentionService,
    private service: DashboardService,
    private authService: AuthService,
    private serviceCollegeYear: CollegeYearService
  ) {}
  async ngAfterViewInit() {
    
  }

  async ngOnInit() {
    let year = localStorage.getItem('collegeYear')
    if(year){
      this.totalDas = await this.service.totaldashboard(year).toPromise()
    }else{
      let allYears = await this.serviceCollegeYear.getDataPromise().toPromise()
      year = allYears[0].title
      this.totalDas = await this.service.totaldashboard(year).toPromise()
    }
    console.log(this.totalDas)
    let totalLicence = this.totalDas.L1 + this.totalDas.L2 + this.totalDas.L3
    console.log(totalLicence, this.totalDas.PL)
    this.percentLicencePassant = (this.totalDas.PL * 100)/ totalLicence
  }
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  fetchData(params?: QueryParams) {
    console.log('ascasc');
   // return this.homeService.getDataObservable(parseQueryParams(params));
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
    console.log(_params);
    this.fetchData(_params)
      ?.pipe(first())
      .subscribe({
        next: (data) => {
          console.log(data);
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
    console.log('ascasc');
    return this.getDataObservable(parseQueryParams(params));
  }
  getDataObservable(params: HttpParams): Observable<any> {
    return this.http.get<any>(`${BASE_URL}/college_year/`,{params: params});
  }
}